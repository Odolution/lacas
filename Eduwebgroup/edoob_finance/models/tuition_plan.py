# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.fields import Command
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

import json
import logging
from random import randint
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

class TuitionPlan(models.Model):
    _name = 'tuition.plan'
    _description = 'Tuition plan'
    _inherit = 'tuition.plan.mixin'

    @api.model
    def default_get(self, fields_list):
        res = super(TuitionPlan, self).default_get(fields_list)
        if 'name' in fields_list:
            res['name'] = '/'
        return res

    @api.model
    def _default_note_url(self):
        return self.env.company.get_base_url()

    @api.model
    def _default_note(self):
        use_invoice_terms = self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms')
        if use_invoice_terms and self.env.company.terms_type == "html":
            baseurl = html_keep_url(self._default_note_url() + '/terms')
            return _('Terms & Conditions: %s', baseurl)
        return use_invoice_terms and self.env.company.invoice_terms or ''

    @api.model
    def _default_color(self):
        return randint(1, 11)

    code = fields.Char()
    active = fields.Boolean(default=True)
    student_id = fields.Many2one('school.student', string="Student", required=True, tracking=True)
    tuition_template_id = fields.Many2one('tuition.template', required=True, ondelete='restrict')
    installment_ids = fields.One2many('tuition.installment', 'tuition_plan_id')
    plan_year = fields.Integer(
        string="Plan year", help="This field will set the year for the first installment",
        required=True, default=lambda self: fields.Date.today().year)

    note = fields.Html('Terms and conditions', default=_default_note)

    line_ids = fields.One2many('tuition.plan.line', 'plan_id')

    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('posted', "Posted"),
            ('cancel', "Cancelled"),
        ], string="State", default='draft', required=True, tracking=True, group_expand='_read_group_state',)
    student_grade_level_ids = fields.Many2many('school.grade.level', string="Student grade levels", store=True, compute='compute_student_grade_levels')
    posted_before = fields.Boolean(default=False)
    next_installment_id = fields.Many2one(
        'tuition.installment', string="Next installment",
        domain="[('id', 'in', installment_ids)]")
    next_installment_date = fields.Date(
        string="Next installment date", store=True,
        related='next_installment_id.real_date')

    sale_order_ids = fields.Many2many(
        'sale.order', store=True, readonly=True,
        relation='tuition_plan_sale_order_rel', column1='tuition_plan_id', column2='sale_order_id')
    sale_order_count = fields.Integer(string="Sale order count", compute='compute_sale_order_count')

    account_move_ids = fields.Many2many(
        'account.move', store=True, readonly=True,
        relation='tuition_plan_account_move_rel', column1='tuition_plan_id', column2='account_move_id')
    account_move_count = fields.Integer(string="Sale order count", compute='compute_account_move_count')

    merge_group_color = fields.Integer(
        string="Merge group",
        help="Merge group. Student that are in the same family will appear together in the invoices")
    student_avatar = fields.Binary(related='student_id.image_128', string="Avatar", store=False)

    tax_totals_json = fields.Char(
        string="Invoice Totals JSON",
        compute='_compute_tax_totals_json',
        readonly=False,
        help='Edit Tax amounts if you encounter rounding issues.')
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, compute='_amount_all', tracking=5)
    amount_tax = fields.Monetary(string='Taxes', store=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, compute='_amount_all', tracking=4)

    @api.depends('line_ids.tax_ids', 'line_ids.unit_price', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        def compute_taxes(line):
            price = line.unit_price * (1 - (line.discount or 0.0) / 100.0)
            line_plan = line.plan_id
            return line.tax_ids._origin.compute_all(price, line_plan.currency_id, line.quantity, product=line.product_id, partner=line_plan.student_id.partner_id)

        account_move = self.env['account.move']
        for plan in self:
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(plan.line_ids, compute_taxes)
            tax_totals = account_move._get_tax_totals(plan.student_id.partner_id, tax_lines_data, plan.amount_total, plan.amount_untaxed, plan.currency_id)
            plan.tax_totals_json = json.dumps(tax_totals)

    @api.depends('line_ids.price_total')
    def _amount_all(self):
        """ Compute the total amounts of the tuition plan. """
        for plan in self:
            amount_untaxed = amount_tax = 0.0
            for line in plan.line_ids:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            plan.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
                })

    def cron_recurring_create_charge(self):
        self.recurring_create_charge(force=False)

    def button_create_charge(self):
        self.recurring_create_charge(force=True)

    def button_confirm(self):
        self.post()

    def button_draft(self):
        self.write({'state': 'draft'})

    def button_cancel(self):
        self.write({'state': 'cancel'})

    def open_update_values_wizard(self):
        context = {'active_ids': self.ids, 'active_model': self._name, **self._context}
        return {
            'name': _("Update tuition plans"),
            'type': 'ir.actions.act_window',
            'res_model': 'update.tuition.plan',
            'view_mode': 'form',
            'target': 'new',
            'context': context
            }

    @api.depends('sale_order_ids')
    def compute_sale_order_count(self):
        for plan in self:
            plan.sale_order_count = len(plan.sale_order_ids)

    @api.depends('account_move_ids')
    def compute_account_move_count(self):
        for plan in self:
            plan.account_move_count = len(plan.account_move_ids)

    @api.depends('student_id', 'student_id.grade_level_ids')
    def compute_student_grade_levels(self):
        for plan in self:
            plan.student_grade_level_ids = plan.student_id.grade_level_ids

    def action_view_sale_order(self):
        sales = self.mapped('sale_order_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
        if len(sales) > 1:
            action['domain'] = [('id', 'in', sales.ids)]
        elif len(sales) == 1:
            form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = sales.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        if len(self) == 1:
            context = {
                'default_sale_origin': self.name,
            }
            action['context'] = context
        return action

    def action_view_account_move(self):
        invoices = self.mapped('account_move_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'out_invoice',
        }
        if len(self) == 1:
            context.update({
                'default_student_id': self.student_id.id,
                'default_invoice_payment_term_id': self.payment_term_id.id or self.student_id.property_payment_term_id.id or
                                                   self.env['account.move'].default_get(
                                                       ['invoice_payment_term_id']).get('invoice_payment_term_id'),
                'default_invoice_origin': self.name,
            })
        action['context'] = context
        return action

    def post(self):
        for plan in self:
            plan._compute_next_installment()
            vals = {
                'posted_before': True,
                'state': 'posted',
            }
            if not plan.posted_before and plan.name == '/':
                sequence = self.env['ir.sequence'].next_by_code('tuition.plan.sequence')
                vals['name'] = sequence
            plan.write(vals)

        if not self.next_installment_id:
            self._compute_next_installment()

    def _compute_next_installment(self):
        for plan in self:
            installments = plan.installment_ids.sorted('sequence')
            next_installment = plan._get_next_installment()

            if not next_installment:
                if self.next_installment_id:
                    next_installment = self.installment_ids.sorted('sequence')[:1]
                else:
                    next_installment = self.installment_ids.filtered(lambda inst: inst.real_date >= fields.Date.today()).sorted('real_date')[:1]
            current_installment = plan.next_installment_id
            if current_installment == installments[-1] and next_installment == installments[0]:
                plan.plan_year = plan._get_next_plan_year()
            plan.next_installment_id = next_installment

    def _get_invoice_delivery_partner_id(self):
        self.ensure_one()
        return self.student_id.partner_id.address_get(['delivery'])['delivery']

    def _get_next_installment(self):
        self.ensure_one()
        next_installment = self.next_installment_id.get_next_installment()
        if not next_installment:
            if self.next_installment_id:
                next_installment = self.installment_ids.sorted('sequence')[:1]
            else:
                next_installment = self.installment_ids.filtered(lambda inst: inst.real_date >= fields.Date.today()).sorted('real_date')[:1]

        return next_installment

    def _find_other_plans_in_same_group(self):
        self.ensure_one()
        if not self.merge_group_color:
            return self
        students = self.student_id.family_ids.mapped('student_ids') - self.student_id
        same_group_plans = self
        for student in students:
            plans = student.tuition_plan_ids.filtered(lambda p: p._is_tuition_pending_to_create_charge())
            for plan in plans:
                try:
                    if plan.next_installment_id.real_date == self.next_installment_id.real_date:
                        (plan.next_installment_id + self.next_installment_id)._ensure_tuition_same_configuration()
                        same_group_plans += plan
                except ValidationError:
                    continue
        return same_group_plans

    def _is_tuition_pending_to_create_charge(self):
        self.ensure_one()
        today = fields.Date.today()
        return self.state == 'posted' and self.next_installment_id and self.next_installment_id.real_date <= today

    def recurring_create_charge(self, force=False):
        if not self:
            return
        for plan in self:
            if force or plan._is_tuition_pending_to_create_charge():
                other_plans = plan._find_other_plans_in_same_group()
                next_installments = other_plans.mapped('next_installment_id')
                if next_installments:
                    next_installments.create_recurring_charge(origin_plan=plan)

    @api.model
    def create(self, vals):
        plan = super().create(vals)
        if self._context.get('take_tuition_template_values', False):
            plan.update_values_based_on_tuition_plan()
        plan.update_lines(overwrite=True)
        return plan

    def update_lines(self, overwrite=False):
        for plan in self:
            line_values_list = plan.tuition_template_id.line_ids.get_tuition_plan_values(student=plan.student_id)
            line_values_list = [Command.create(vals) for vals in line_values_list]
            if overwrite:
                line_values_list.insert(0, Command.clear())
            plan.write({'line_ids': line_values_list})

    def update_installments(self, overwrite=False):
        for plan in self:
            tuition_template = plan.tuition_template_id
            installment_values_list = [Command.create(installment_values) for installment_values in tuition_template.installment_ids.get_installment_values()]
            if overwrite:
                installment_values_list.insert(0, Command.clear())
            plan.write({'installment_ids': installment_values_list})

    def update_values_based_on_tuition_plan(self):
        for plan in self:
            tuition_template = plan.tuition_template_id
            installment_values_list = [Command.create(installment_values) for installment_values in tuition_template.installment_ids.get_installment_values()]
            plan.update({
                'installment_ids': [Command.clear(), *installment_values_list],
                'journal_id': tuition_template.journal_id.id,
                'invoice_method': tuition_template.invoice_method,
                'post_action_option': tuition_template.post_action_option,
                'fiscal_position_id': tuition_template.fiscal_position_id.id,
                'tax_country_id': tuition_template.tax_country_id.id,
                'analytic_account_id': tuition_template.analytic_account_id.id,
                'sale_mail_template_id': tuition_template.sale_mail_template_id.id,
                'invoice_mail_template_id': tuition_template.invoice_mail_template_id.id,
                'payment_term_id': tuition_template.payment_term_id.id,
                'pricelist_option': tuition_template.pricelist_option,
                'pricelist_id': tuition_template.pricelist_id.id,
                })

    @api.model
    def _read_group_state(self, states, domain, order):
        return list(dict(self._fields['state'].selection).keys())

    def update_prices(self):
        pricelist = self.get_pricelist()
        for line in self.line_ids:
            if line.is_in_pricelist(pricelist):
                line.update_pricelist_data(pricelist)
            else:
                line.unit_price = line.template_line_id.unit_price or line.product_id.lst_price

    def get_pricelist_partner(self, family=False):
        """
        :return: False if there is no unique partner
        """
        if self.pricelist_option in ('student', 'fixed_pricelist', 'fixed_prices'):
            return self.student_id
        elif self.pricelist_option == 'invoice_address':
            if family:
                return family.invoice_address_id
            else:
                _logger.warning("No family when invoice_address_id is a option!")
        return False

    def get_pricelist(self, family=False, *args, **kwargs):
        self.ensure_one()
        if self.pricelist_option == 'student':
            return self.student_id.property_product_pricelist
        elif self.pricelist_option == 'fixed_pricelist':
            return self.pricelist_id
        elif self.pricelist_option == 'invoice_address' and family:
            if not family.invoice_address_id:
                raise UserError(_("The family %s doesn't have a invoice address"))
            return family.invoice_address_id.property_product_pricelist
        return False

    def set_installments_to_template(self):
        self.update_installments(overwrite=True)

    def set_lines_to_template(self):
        self.update_lines(overwrite=True)

    def _get_next_plan_year(self):
        """
        Why current year instead of next year?
        This is because we need to allow some configuration which installment can go over a lot of years
        In these cases, we need to keep the initial year until the last year is invoked. The last installment will be invoked in the next year.
        :return: The next year based on the installment real date but with today's year
        """
        self.ensure_one()
        if not self.installment_ids:
            return False
        first_installment_real_date = self.installment_ids[:1].real_date
        today = fields.Date.today()
        first_installment_real_date += relativedelta(year=today.year)
        return first_installment_real_date.year + 1 if first_installment_real_date < today else first_installment_real_date.year
