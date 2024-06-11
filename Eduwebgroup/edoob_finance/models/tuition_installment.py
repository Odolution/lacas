# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError
from odoo.fields import Command

import datetime
from dateutil.relativedelta import relativedelta


class TuitionPlanInstallment(models.Model):
    _name = "tuition.installment"
    _inherit = 'tuition.installment.mixin'
    _description = "Tuition Plan Installment"

    date = fields.Date(
        string="Date", help="Date to trigger installment", required=True, default=lambda self: fields.Date.today())
    tuition_plan_id = fields.Many2one("tuition.plan", "Tuition Plan", required=True, ondelete="cascade")
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('post', "Posted"),
            ('cancel', "Cancelled"),
        ], string="State", required=True, default='draft')

    lines_ids = fields.Many2many(
        'tuition.plan.line',
        relation='tuition_installment_extra_services_rel',
        column1='installment_id',
        column2='line_id',
        string="Lines")
    template_installment_id = fields.Many2one('tuition.template.installment', string="Template installment")

    def create_recurring_charge(self, origin_plan=False):
        """ It creates sale order or invoice """
        self._ensure_tuition_same_configuration()
        if not origin_plan:
            origin_plan = self[0].tuition_plan_id

        # We can use the first because the ensure method above
        plan = self[0].tuition_plan_id
        default_journal = plan.journal_id
        journals = self.lines_ids.mapped(lambda l: l.journal_id or default_journal) | self.mapped('tuition_plan_id.journal_id')

        # We filter by journal and put in the default journal those lines that haven't journal_id set
        lines_by_journals = {journal: self.lines_ids.filtered(lambda l: (l.journal_id or default_journal) == journal) for journal in journals}
        charges = False
        for journal, lines in lines_by_journals.items():
            if plan.invoice_method == 'sale':
                charges = self.create_sale_orders(lines, journal, origin_plan)
            elif plan.invoice_method == 'move':
                charges = self.create_invoices(lines, journal, origin_plan)
        if charges:
            self._do_post_action(plan, charges)
            self.mapped('tuition_plan_id')._compute_next_installment()

    def _ensure_tuition_same_configuration(self):
        if not self:
            raise ValidationError(_("At least one installment installment is needed to create sale orders/invoices"))
        if len(self) == 1:
            return
        plans = self.mapped('tuition_plan_id')
        invoice_methods = set(plans.mapped('invoice_method'))
        post_action_option = set(plans.mapped('post_action_option'))
        merge_groups = set(plans.mapped('merge_group_color'))
        analytic_accounts = set(plans.mapped('analytic_account_id'))
        pricelists = set(plans.mapped('pricelist_id'))
        fiscal_positions = set(plans.mapped('fiscal_position_id'))
        sale_mail_templates = set(plans.mapped('sale_mail_template_id'))
        invoice_mail_templates = set(plans.mapped('invoice_mail_template_id'))
        dates = set(self.mapped('real_date'))
        if len(invoice_methods) != 1:
            raise ValidationError(_("Tuition plans don't have the same invoice method!"))
        if len(post_action_option) > 1:
            raise ValidationError(_("Tuition plans don't have the same post-action option!"))
        if len(merge_groups) != 1:
            raise ValidationError(_("Tuition plans don't belong to the same merge group!"))
        if len(analytic_accounts) > 1:
            raise ValidationError(_("Tuition plans don't have to the same analytic account!"))
        if len(pricelists) > 1:
            raise ValidationError(_("Tuition plans don't have to the same pricelist!"))
        if len(fiscal_positions) > 1:
            raise ValidationError(_("Tuition plans don't have to the same fiscal position!"))
        if len(sale_mail_templates) != 1:
            raise ValidationError(_("Tuition plans don't have to the same sale mail template!"))
        if len(invoice_mail_templates) != 1:
            raise ValidationError(_("Tuition plans don't have to the same invoice mail template!"))
        if len(dates) != 1:
            raise ValidationError(_("Installment doesn't have same real date!"))

    def create_sale_orders(self, lines, journal, origin_plan=False):
        vals_list = self._prepare_sale_order_values(lines, journal, origin_plan)
        return self.env['sale.order'].create(vals_list)

    def _prepare_sale_order_values(self, lines, journal, origin_plan=False):
        self._ensure_tuition_same_configuration()
        plan = origin_plan or self[0].tuition_plan_id
        students = self.mapped('tuition_plan_id.student_id')
        families = students.mapped('family_ids')
        real_date = self[0].real_date

        invoice_date = self[0].real_date

        sale_vals_list = []

        # We build several sale order depending on
        for family in families:
            if not family.invoice_address_id:
                raise UserError(_("Family %s[%s] doesn't have an invoice address!", family.name, family.id))
            sale_vals = self._prepare_sale_order_for_family(plan, journal, family, lines, real_date, invoice_date)
            if not sale_vals:
                continue
            sale_vals_list.append(sale_vals)

        return sale_vals_list

    def _prepare_sale_order_for_family(self, plan, journal, family, lines, real_date, invoice_date):
        order_line_vals = []
        for line in lines.filtered(lambda l: family in l.plan_id.student_id.family_ids):
            line_vals = line.prepare_sale_order_values(family)
            if line_vals["price_unit"]:
                order_line_vals.append(Command.create(line_vals))
        if not order_line_vals:
            return False
        if not family.invoice_address_id:
            raise UserError(_("The family %s doesn't have invoice address!", family.name))

        sale_pricelist = plan.get_pricelist(family)
        sale_vals = {
            "date_order": invoice_date,
            "partner_id": family.invoice_address_id.id,
            "family_id": family.id,
            "analytic_account_id": plan.analytic_account_id.id,
            "order_line": order_line_vals,
            "origin": ",".join(self.mapped('tuition_plan_id.name')),
            'company_id': plan.company_id.id,
            'edoob_finance_journal_id': journal.id,
            'payment_term_id': plan.payment_term_id.id,
            'installment_real_date': real_date,
            'tuition_plan_ids': [Command.set(self.mapped('tuition_plan_id').ids)],
            }
        if sale_pricelist:
            sale_vals['pricelist_id'] = sale_pricelist.id
        return sale_vals

    def create_invoices(self, lines, journal, origin_plan=False):
        vals_list = self._prepare_invoice_values(lines, journal, origin_plan)
        return self.env['account.move'].create(vals_list)

    def _prepare_invoice_values(self, lines, journal, origin_plan=False):
        self._ensure_tuition_same_configuration()
        plan = origin_plan or self[0].tuition_plan_id
        invoice_date = self[0].real_date
        real_date = self[0].real_date
        move_vals_list = []
        # We build several sale move depending on
        for family in origin_plan.student_id.family_ids:
            if not family.invoice_address_id:
                raise UserError(_("Family %s[%s] doesn't have an invoice address!", family.name, family.id))
            move_vals = self._prepare_invoice_values_for_family(plan, journal, family, lines, real_date, invoice_date)
            if not move_vals:
                continue
            move_vals_list.append(move_vals)
        return move_vals_list

    def _prepare_invoice_values_for_family(self, plan, journal, family, lines, real_date, invoice_date):
        move_line_vals = []
        for line in lines.filtered(lambda l: family in l.plan_id.student_id.family_ids):
            line_vals = line.prepare_invoice_line_values(family)
            if line_vals["price_unit"]:
                move_line_vals.append(Command.create(line_vals))
        if not move_line_vals:
            return False
        if not family.invoice_address_id:
            raise UserError(_("The family %s doesn't have invoice address!", family.name))

        move_vals = {
            'move_type': 'out_invoice',
            'invoice_date': invoice_date,
            'partner_id': family.invoice_address_id.id,
            'family_id': family.id,
            'invoice_line_ids': move_line_vals,
            'company_id': plan.company_id.id,
            'tuition_plan_ids': [Command.set(self.mapped('tuition_plan_id').ids)],
            'journal_id': journal.id,
            'invoice_payment_term_id': plan.payment_term_id.id,
            'installment_real_date': real_date,
            }
        return move_vals

    def should_generate_invoices_for_family(self, family):
        invoices = self.mapped('tuition_plan_id.account_move_ids').filtered_domain([('family_id', '=', family.id)])
        if not invoices:
            return True
        for invoice in invoices:
            if invoice.installment_real_date == self[0].real_date:
                return False
        return True

    def should_generate_sale_orders_for_family(self, family):
        sale_orders = self.mapped('tuition_plan_id.sale_order_ids').filtered_domain([('family_id', '=', family.id)])
        if not sale_orders:
            return True
        for order in sale_orders:
            if order.installment_real_date == self[0].real_date:
                return False
        return True

    @api.model
    def _do_post_action(self, plan, charges):
        if plan.post_action_option in ('confirm', 'confirm_send'):
            self._confirm_records(charges)
        if plan.post_action_option in ('send', 'confirm_send'):
            self._send_records(plan, charges)

    @api.model
    def _confirm_records(self, charges):
        if charges._name == 'sale.order':
            charges.action_confirm()
        elif charges._name == 'account.move':
            charges.action_post()

    @api.model
    def _send_records(self, plan, charges):
        if charges._name == 'sale.order':
            self._send_mail_to_record(plan.sale_mail_template_id, charges)
        elif charges._name == 'account.move':
            self._send_mail_to_record(plan.invoice_mail_template_id, charges)

    def _send_mail_to_record(self, mail_template, records):
        plans = self.mapped('tuition_plan_id')
        for record in records:
            email_context = {
                'plans': plans,
            }
            mail_template.with_context(email_context).send_mail(record.id)
        if records._name == 'sale.order':
            records.filtered(lambda r: r.state == 'draft').action_quotation_sent()
        elif records._name == 'account.move':
            records.sudo().write({'is_move_sent': True})

    def _get_monthly_date(self):
        self.ensure_one()
        if not self.month:
            return False
        plan_year = self.tuition_plan_id.plan_year
        if self.day_type == 'last_day':
            day = 31
        elif self.day_type == 'day_number':
            day = int(self.day_of_the_month)
        else:
            day = 1
        next_date = datetime.date(year=plan_year, month=1, day=1) + relativedelta(month=int(self.month), day=day)
        next_date = self.move_next_year_if_needed(next_date)
        return next_date

    def get_previous_installment(self):
        sorted_sibling_installments = self.tuition_plan_id.installment_ids.sorted('sequence')
        previous_installment = self.browse()
        for i, installment in enumerate(sorted_sibling_installments):
            if i == 0 and installment == self:
                break
            elif installment == self:
                previous_installment = sorted_sibling_installments[i - 1]
        return previous_installment

    def get_next_installment(self):
        sorted_sibling_installments = self.tuition_plan_id.installment_ids.sorted('sequence', reverse=True)
        next_installment = self.browse()
        for i, installment in enumerate(sorted_sibling_installments):
            if i == 0 and installment == self:
                break
            elif installment == self:
                next_installment = sorted_sibling_installments[i - 1]
        return next_installment

    def get_parent(self):
        self.ensure_one()
        return self.tuition_plan_id
