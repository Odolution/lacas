# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError
from odoo.fields import Command

import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

import json
import logging
from random import randint

from odoo.tools.safe_eval import safe_eval

from babel.dates import format_date
import json
from datetime import datetime, timedelta
from odoo.tools.misc import get_lang
import random



_logger = logging.getLogger(__name__)


# ol.finance.model

class OlFinanceUtil(models.AbstractModel):
    _name = 'ol.finance.util'
    _description = "ol finance util"

    @api.model
    def _get_family_percentage(self, student, family, product):
        parent_category_id = product.categ_id
        available_categories = student.mapped('financial_responsibility_ids.product_category_id')

        while parent_category_id:
            if parent_category_id in available_categories:
                break
            parent_category_id = parent_category_id.parent_id

        if not parent_category_id:
            raise UserError(_("%s[%s] doesn't have a responsible family for %s", student.name, student.id, parent_category_id.complete_name))

        percentage_sum = sum([category.percentage for category in student.financial_responsibility_ids if
                              category.product_category_id == parent_category_id and category.family_id == family])
        return percentage_sum

    @api.model
    def _get_real_price_currency(self, product, rule_id, quantity, uom, date, company):
        """Retrieve the price before applying the pricelist
                    :param obj product: object of current product record
                    :parem float qty: total quentity of product
                    :param tuple price_and_rule: tuple(price, suitable_rule) coming from pricelist computation
                    :param obj uom: unit of measure of current order line"""
        PricelistItem = self.env['product.pricelist.item']
        field_name = 'lst_price'
        currency_id = None
        product_currency = product.currency_id
        if rule_id:
            pricelist_item = PricelistItem.browse(rule_id)
            if pricelist_item.pricelist_id.discount_policy == 'without_discount':
                while pricelist_item.base == 'pricelist' and pricelist_item.base_pricelist_id and pricelist_item.base_pricelist_id.discount_policy == 'without_discount':
                    _price, rule_id = pricelist_item.base_pricelist_id.with_context(uom=uom.id).get_product_price_rule(product, quantity, product)
                    pricelist_item = PricelistItem.browse(rule_id)

            if pricelist_item.base == 'standard_price':
                field_name = 'standard_price'
                product_currency = product.cost_currency_id
            elif pricelist_item.base == 'pricelist' and pricelist_item.base_pricelist_id:
                field_name = 'price'
                product = product.with_context(pricelist=pricelist_item.base_pricelist_id.id)
                product_currency = pricelist_item.base_pricelist_id.currency_id
            currency_id = pricelist_item.pricelist_id.currency_id

        if not currency_id:
            currency_id = product_currency
            cur_factor = 1.0
        else:
            if currency_id.id == product_currency.id:
                cur_factor = 1.0
            else:
                cur_factor = currency_id._get_conversion_rate(product_currency, currency_id, company, date)

        product_uom = self.env.context.get('uom') or product.uom_id.id
        if uom and uom.id != product_uom:
            # the unit price is in a different uom
            uom_factor = uom._compute_price(1.0, product.uom_id)
        else:
            uom_factor = 1.0

        return product[field_name] * uom_factor * cur_factor, currency_id

    @api.model
    def _get_pricelist_price(self, pricelist, product, quantity, product_uom, partner, date, company, currency, fiscal_position_id):
        return product._get_tax_included_unit_price(company, currency,
            date,
            'sale',
            fiscal_position=self.order_id.fiscal_position_id,
            product_price_unit=self._get_display_price(product),
            product_currency=self.order_id.currency_id
            )
        return pricelist.get_product_price(product, quantity, partner, date, product_uom)

    @api.model
    def _get_pricelist_discount(self, pricelist, product, quantity, product_uom, partner, date, company):

        if not (pricelist.discount_policy == 'without_discount' and self.env.user.has_group('product.group_discount_per_so_line')):
            return

        discount = 0.0
        product = product.with_context(
            lang=partner.lang,
            partner=partner,
            quantity=quantity,
            date=date,
            pricelist=pricelist.id,
            uom=product_uom.id,
            fiscal_position=self.env.context.get('fiscal_position', False))

        product_context = dict(self.env.context, partner_id=partner.id, date=date, uom=product_uom.id)

        price, rule_id = pricelist.with_context(product_context).get_product_price_rule(product, quantity or 1.0, partner)
        new_list_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, quantity, product_uom, date, company)

        if new_list_price != 0:
            if pricelist.currency_id != currency:
                new_list_price = currency._convert(new_list_price, pricelist.currency_id, company or self.env.company, date or fields.Date.today())
            discount = (new_list_price - price) / new_list_price * 100
        return discount

    @api.model
    def get_pricelist_price_data(self, pricelist, product, quantity, product_uom, partner, date, company=False, fiscal_position=False):
        if not company:
            company = self.env.company
        if not fiscal_position:
            fiscal_position = self.env.context.get('fiscal_position', False)

        if company:
            self = self.with_company(company)

        if not product_uom or product.uom_id.category_id.id != product_uom.category_id.id:
            product_uom = product.uom_id

        product = product.with_context(
            lang=partner.lang,
            partner=partner,
            date=date,
            fiscal_position=fiscal_position,
            pricelist=pricelist.id,
            quantity=quantity,
            uom=product_uom.id
            )
        pricelist_price = product.price     # Price according to pricelist in pricelist currency in self.uom
        base_price = product.lst_price      # Base price of the product in self.uom

        if product.currency_id != pricelist.currency_id:
            base_price = product.currency_id._convert(base_price, pricelist.currency_id, product.company_id or self.env.company, fields.Date.today())

        if pricelist.discount_policy == 'without_discount' and pricelist_price:
            discount = max(0, (base_price - pricelist_price) * 100 / base_price)
            product_price = base_price
        else:
            product_price = pricelist_price
            discount = 0

        return {
            'product_price': product_price,
            'discount': discount,
            }

# tuition.installment

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
            'ol_finance_journal_id': journal.id,
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
        value = origin_plan.student_id.relationship_ids
        if not value:
            raise UserError(_("Their is no Relationship on olf id: [%s], Student: [%s]", origin_plan.student_id.olf_id, origin_plan.student_id.name))
        # We build several sale move depending on
        for family in origin_plan.student_id.family_ids:
            if not family.invoice_address_id:
                raise UserError(_("Family %s[%s] doesn't have an invoice address!", family.name, family.id))
            move_vals = self._prepare_invoice_values_for_family(plan, journal, family, lines, real_date, invoice_date,value)
            if not move_vals:
                continue
            move_vals_list.append(move_vals)
        return move_vals_list

    def _prepare_invoice_values_for_family(self, plan, journal, family, lines, real_date, invoice_date,value):
        move_line_vals = []
        id = 0
        for line in lines.filtered(lambda l: family in l.plan_id.student_id.family_ids):
            line_vals = line.prepare_invoice_line_values(family)
            if line_vals["price_unit"]:
                move_line_vals.append(Command.create(line_vals))
        if not move_line_vals:
            return False
        if not family.invoice_address_id:
            raise UserError(_("The family %s doesn't have invoice address!", family.name))
        for rec in value:
            if rec:
                if rec.relationship_type_id.name == "Father":
                    id = rec.individual_id.partner_id.id
                    break
                else:
                    id = rec.individual_id.partner_id.id
                    break
            else:
                id = family.invoice_address_id.id
                
        move_vals = {
            'move_type': 'out_invoice',
            'invoice_date': invoice_date,
            'partner_id': id,
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
        next_date = date(year=plan_year, month=1, day=1) + relativedelta(month=int(self.month), day=day)
        # next_date = datetime.date(year=plan_year, month=1, day=1) + relativedelta(month=int(self.month), day=day)
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


# tuition.plan.discount

# class TuitionPlanDiscount(models.Model):
#     _name = "tuition.plan.discount"
#     _description = "Tuition plan discount"

# tuition.plan.line 

class ConcessionLine(models.Model):
    _name = "concession.plan.line"

    student_id = fields.Many2one('school.student', string="Student", ondelete='set null')

    discount_name    = fields.Many2one('ol.discount.charges', string="Discount name")
    discount_product = fields.Many2one('product.product', string="Discount Product")

    #logic start
    @api.onchange('discount_name')
    def _onchange_discount(self):
        for rec in self:
            rec.discount_product = rec.discount_name.product_id
    

    def get_concession_values(self,installment_obj):
        values = []

        for line in self:
            lst = []
            
            for j in installment_obj:
                # raise UserError(j.ids)
                lst.append(j.id)

            values.append({
                
                'product_id'        : line.discount_product.id,
                'name'              : line.discount_product.name,
                'quantity'          : 1,
                'unit_price'        : 0,
                'currency_id'       : line.student_id.currency_id.id,
                'installment_ids'   : [(6,0,lst)],
                # 'discount_charges'  : True,

            })
        # raise UserError(str(values))
        return values
    #logic end



class TuitionPlanLine(models.Model):
    _name = 'tuition.plan.line'
    _inherit = 'tuition.line.mixin'
    _description = "Tuition plan line"

    plan_id = fields.Many2one('tuition.plan', required=True, ondelete='cascade')

    plan_pricelist_option = fields.Selection(related='plan_id.pricelist_option')
    plan_pricelist_id = fields.Many2one('product.pricelist', related='plan_id.pricelist_id')
    student_families = fields.Many2many('school.family', related='plan_id.student_id.family_ids')

    plan_installment_ids = fields.One2many('tuition.installment', related='plan_id.installment_ids')
    template_installment_ids = fields.Many2many(
        'tuition.template.installment', related='template_line_id.installment_ids')
    installment_ids = fields.Many2many(
        'tuition.installment', string="Installments",
        relation='tuition_installment_extra_services_rel',
        column1='line_id',
        column2='installment_id',
        domain="[('id', 'in', plan_installment_ids)]")
    template_line_id = fields.Many2one('tuition.template.line')
    form_create_mode = fields.Boolean(compute='_compute_form_create_mode')

    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position',
        check_company=True, domain="[('company_id', '=', company_id)]",
        ondelete="restrict",
        help="Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices. "
             "The default value comes from the customer.")
    company_id = fields.Many2one('res.company', related='plan_id.company_id')

    # process end 
    discount_charges = fields.Boolean('Discount Charges') 
    # process start 

    # ==========================
    # Compute & onchange methods
    # ==========================
    @api.constrains('installment_ids')
    def _constraint_installment_ids(self):
        for line in self:
            for installment in line.installment_ids:
                if installment.tuition_plan_id not in line.plan_id:
                    raise ValidationError(_("A line has an installment from other tuition plan!"))

    def _compute_form_create_mode(self):
        for line in self:
            line.form_create_mode = not line.plan_id._origin

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            # if not line.product_id or line.display_type in ('line_section', 'line_note'):
            #     continue
            line.name = line._get_computed_name()
            taxes = line._get_computed_taxes()
            if taxes and line.plan_id.fiscal_position_id:
                taxes = line.plan_id.fiscal_position_id.map_tax(taxes)
            line.tax_ids = taxes
            line.product_uom_id = line._get_computed_uom()
            line.unit_price = line._get_computed_price_unit()
            line.account_id = line._get_computed_account()

    # ===========
    # CRUD Method
    # ===========
    @api.model
    def create(self, values):
        res = super(TuitionPlanLine, self).create(values)
        if res.template_line_id:
            res.reset_installment_ids()
        return res

    # =================
    # Business methods
    # =================
    def reset_installment_ids(self):
        for line in self:
            template_installment_ids = line.template_line_id.installment_ids
            line.installment_ids = line.plan_id.installment_ids.filtered(lambda inst: inst.template_installment_id in template_installment_ids)

    def _get_product_pricelist_price_and_discount(self, family=False):
        if not family or self.plan_id.pricelist_option == 'fixed_prices':
            return self.unit_price, self.discount

        pricelist = self.plan_id.get_pricelist(family)
        partner = self.plan_id.get_pricelist_partner(family)

        product = self.product_id
        quantity = self.quantity
        product_uom = self.product_uom_id
        partner = partner
        date = self.plan_id.next_installment_id.real_date
        company = self.company_id

        pricelist_data = self.env['ol.finance.util'].get_pricelist_price_data(
            pricelist=pricelist,
            product=product,
            quantity=quantity,
            product_uom=product_uom,
            partner=partner,
            date=date,
            company=company,
            fiscal_position=partner.property_account_position_id)

        price = pricelist_data['product_price']
        discount = pricelist_data['discount']
        return price, discount

    def prepare_sale_order_values(self, family=False):
        price, discount = self._get_product_pricelist_price_and_discount(family)
        percentage = self.env['ol.finance.util']._get_family_percentage(self.plan_id.student_id, family, self.product_id)
        return {
            'product_id': self.product_id.id,
            'name': self.name,
            'product_uom_qty': self.quantity,
            'price_unit': price * percentage,
            'discount': discount,
            'tax_id': [Command.set(self.tax_ids.ids)],
            'student_id': self.plan_id.student_id.id,
            'tuition_plan_id': self.plan_id.id,
            'analytic_tag_ids': [Command.set(self.analytic_tag_ids.ids)],
        }

    def prepare_invoice_line_values(self, family=False):
        self.ensure_one()
        price, discount = self._get_product_pricelist_price_and_discount(family)
        percentage = self.env['ol.finance.util']._get_family_percentage(self.plan_id.student_id, family, self.product_id)
        return {
            'product_id': self.product_id.id,
            'account_id': self.account_id.id,
            'name': self.name,
            'quantity': self.quantity,
            'price_unit': price * percentage,
            'discount': discount,
            'tax_ids': [Command.set(self.tax_ids.ids)],
            'student_id': self.plan_id.student_id.id,
            'tuition_plan_id': self.plan_id.id,
            'analytic_account_id': self.analytic_account_id.id,
            'analytic_tag_ids': [Command.set(self.analytic_tag_ids.ids)],
        }

    def _get_computed_name(self):
        self.ensure_one()

        if self.plan_id.student_id.lang:
            product = self.product_id.with_context(lang=self.plan_id.student_id.lang)
        else:
            product = self.product_id

        values = []
        if product.partner_ref:
            values.append(product.partner_ref)
        if self.journal_id.type == 'sale':
            if product.description_sale:
                values.append(product.description_sale)
        return '\n'.join(values)

    def _get_computed_taxes(self):
        self.ensure_one()
        # Out invoice.
        if self.product_id.taxes_id:
            tax_ids = self.product_id.taxes_id.filtered(lambda tax: tax.company_id == self.plan_id.company_id)
        elif self.account_id.tax_ids:
            tax_ids = self.account_id.tax_ids
        else:
            tax_ids = self.env['account.tax']
        if not tax_ids:
            tax_ids = self.plan_id.company_id.account_sale_tax_id
        if self.company_id and tax_ids:
            tax_ids = tax_ids.filtered(lambda tax: tax.company_id == self.company_id)
        return tax_ids

    def _get_computed_uom(self):
        self.ensure_one()
        if self.product_id:
            return self.product_id.uom_id
        return False

    def _get_computed_account(self):
        self.ensure_one()
        self = self.with_company(self.plan_id.journal_id.company_id)

        if not self.product_id:
            return

        fiscal_position = self.plan_id.fiscal_position_id
        accounts = self.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
        return accounts['income'] or self.account_id

    def _get_computed_price_unit(self):
        self.ensure_one()

        if not self.product_id:
            return 0.0

        company = self.plan_id.company_id
        currency = self.plan_id.currency_id
        company_currency = company.currency_id
        product_uom = self.product_id.uom_id
        fiscal_position = self.plan_id.fiscal_position_id
        move_date = fields.Date.context_today(self)

        product_price_unit = self.product_id.lst_price
        product_taxes = self.product_id.taxes_id.filtered(lambda tax: tax.company_id == company)

        # Apply unit of measure.
        if self.product_uom_id and self.product_uom_id != product_uom:
            product_price_unit = product_uom._compute_price(product_price_unit, self.product_uom_id)

        # Apply fiscal position.
        if product_taxes and fiscal_position:
            product_taxes_after_fp = fiscal_position.map_tax(product_taxes)

            if set(product_taxes.ids) != set(product_taxes_after_fp.ids):
                flattened_taxes_before_fp = product_taxes._origin.flatten_taxes_hierarchy()
                if any(tax.price_include for tax in flattened_taxes_before_fp):
                    taxes_res = flattened_taxes_before_fp.compute_all(
                        product_price_unit,
                        quantity=1.0,
                        currency=company_currency,
                        product=self.product_id,
                        partner=self.plan_id.student_id,
                        is_refund=False,
                    )
                    product_price_unit = company_currency.round(taxes_res['total_excluded'])

                flattened_taxes_after_fp = product_taxes_after_fp._origin.flatten_taxes_hierarchy()
                if any(tax.price_include for tax in flattened_taxes_after_fp):
                    taxes_res = flattened_taxes_after_fp.compute_all(
                        product_price_unit,
                        quantity=1.0,
                        currency=company_currency,
                        product=self.product_id,
                        partner=self.plan_id.student_id,
                        is_refund=False,
                        handle_price_include=False,
                    )
                    for tax_res in taxes_res['taxes']:
                        tax = self.env['account.tax'].browse(tax_res['id'])
                        if tax.price_include:
                            product_price_unit += tax_res['amount']

        # Apply currency rate.
        if currency and currency != company_currency:
            product_price_unit = company_currency._convert(product_price_unit, currency, company, move_date)

        return product_price_unit

    def is_in_pricelist(self, pricelist):
        if not pricelist:
            return False
        self.ensure_one()
        partner = self.env.user.partner_id
        product = self.product_id
        products_qty_partner = [(product, self.quantity, partner)]
        date = self._context.get('date') or fields.Datetime.now()
        uom_id = self.product_uom_id
        category_ids = self._get_product_categories()
        prod_ids = product.ids
        prod_tmpl_ids = product.product_tmpl_id.ids
        items = pricelist._compute_price_rule_get_items(products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids, category_ids)
        return bool(items)

    def _get_product_categories(self):
        category_ids = {}
        category = self.product_id.categ_id
        while category:
            category_ids[category.id] = True
            category = category.parent_id
        return list(category_ids)

    def action_show_family_prices(self):
        self.ensure_one()
        prices = self.sudo().get_student_families_prices_ids()
        return {
            'name': _("Family prices"),
            'type': 'ir.actions.act_window',
            'res_model': 'tuition.plan.family.prices',
            'view_mode': 'list',
            'target': 'new',
            'views': [(self.env.ref('ol_school_account.tuition_plan_family_prices_view_tree').id, 'list')],
            'domain': [('id', 'in', prices.ids)],
        }

    def get_student_families_prices_ids(self):
        self.ensure_one()
        prices = self.env['tuition.plan.family.prices']
        for family in self.student_families:
            prices += prices.create({
                'line_id': self.id,
                'family_id': family.id,
            })
        return prices

    def update_pricelist_data(self, pricelist):
        self.ensure_one()
        partner = self.plan_id.get_pricelist_partner()
        if partner:
            product = self.product_id
            quantity = self.quantity
            product_uom = self.product_uom_id
            date = self.plan_id.next_installment_id.real_date
            company = self.company_id
            fiscal_position = self.fiscal_position_id
            pricelist_data = self.env['ol.finance.util'].get_pricelist_price_data(
                pricelist=pricelist,
                product=product,
                quantity=quantity,
                product_uom=product_uom,
                parnter=partner,
                date=date,
                company=company,
                fiscal_position=fiscal_position)
            self.unit_price = pricelist_data['product_price']
            self.discount = pricelist_data['discount']


    #logic start

    @api.onchange('installment_template')
    def onchange_installment_template(self):
        self.ensure_one()
        self.line_ids.installment_ids = False
        if self.installment_template == 'quarterly':
            self.set_quarterly_installment()
        elif self.installment_template == 'monthly':
            self.set_monthly_installment()
        elif self.installment_template == 'biannually':
            self.set_biannually_installment()
        elif self.installment_template == 'yearly':
            self.set_yearly_installment()

    def set_quarterly_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q1',
                    'month': '9',
                    'day_type': 'first_day',
                    'sequence': 1
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q2',
                    'month': '12',
                    'day_type': 'first_day',
                    'sequence': 2
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q3',
                    'month': '3',
                    'day_type': 'first_day',
                    'sequence': 3
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q4',
                    'month': '6',
                    'day_type': 'first_day',
                    'sequence': 4
                    }),
                ]

    def set_monthly_installment(self):
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'monthly',
                    'month': '1',
                    'day_type': 'first_day',
                    'sequence': 1,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '2',
                    'day_type': 'first_day',
                    'sequence': 2,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '3',
                    'day_type': 'first_day',
                    'sequence': 3,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '4',
                    'day_type': 'first_day',
                    'sequence': 4,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '5',
                    'day_type': 'first_day',
                    'sequence': 5,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '6',
                    'day_type': 'first_day',
                    'sequence': 6,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '7',
                    'day_type': 'first_day',
                    'sequence': 7,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '8',
                    'day_type': 'first_day',
                    'sequence': 8,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '9',
                    'day_type': 'first_day',
                    'sequence': 9,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '10',
                    'day_type': 'first_day',
                    'sequence': 10,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '11',
                    'day_type': 'first_day',
                    'sequence': 11,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '12',
                    'day_type': 'first_day',
                    'sequence': 12,
                    }),
                ]

    def set_biannually_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'biannually',
                    'month': '9',
                    'sequence': 1,
                    }),
                Command.create({
                    'type': 'biannually',
                    'month': '1',
                    'sequence': 2,
                    }),
                ]

    def set_yearly_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'yearly',
                    'month': '1',
                    'day_type': 'first_day',
                    'sequence': 1,
                    }),
                ]

    #logic end
class TuitionPlanFamilyPrices(models.TransientModel):
    _name = 'tuition.plan.family.prices'
    _rec_name = 'price'

    line_id = fields.Many2one('tuition.plan.line', required=True)
    family_id = fields.Many2one('school.family', required=True)
    price = fields.Char(compute='_compute_pricelist_data')
    discount = fields.Char(compute='_compute_pricelist_data')
    invoice_address_id = fields.Many2one('res.partner', store=False, related='family_id.invoice_address_id')

    def get_pricelist(self):
        self.ensure_one()
        return self.family_id.invoice_address_id.property_product_pricelist

    def _compute_price(self):
        for price in self:
            invoice_address = price.family_id.invoice_address_id
            if not invoice_address:
                price.price = _("No invoice address!")
            else:
                pricelist = price.get_pricelist()
                if price.line_id.is_in_pricelist(pricelist):
                    price.price = str(pricelist.get_product_price(
                        price.line_id.product_id, price.line_id.quantity, price.line_id.plan_id.student_id.partner_id))
                else:
                    price.price = str(price.line_id.template_line_id.unit_price or price.line_id.product_id.lst_price)

    def _compute_pricelist_data(self):
        for price in self:

            if not price.invoice_address_id:
                price.price = _("No invoice address!")
                price.discount = _("No invoice address!")
            else:
                pricelist = price.get_pricelist()
                if price.line_id.is_in_pricelist(pricelist):
                    product = price.line_id.product_id
                    quantity = price.line_id.quantity
                    product_uom = price.line_id.product_uom_id
                    partner = price.invoice_address_id
                    date = price.line_id.plan_id.next_installment_id.real_date
                    company = price.line_id.company_id

                    pricelist_data = self.env['ol.finance.util'].get_pricelist_price_data(
                        pricelist=pricelist,
                        product=product,
                        quantity=quantity,
                        product_uom=product_uom,
                        partner=partner,
                        date=date,
                        company=company,
                        fiscal_position=partner.property_account_position_id)

                    price.discount = pricelist_data['discount']
                    price.price = pricelist_data['product_price']
                else:
                    price.price = str(price.line_id.template_line_id.unit_price or price.line_id.product_id.lst_price)
                    price.discount = str(price.line_id.template_line_id.discount)

# tuition.plan

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

    # process start

    # discount_ids = fields.Many2many('ol.discount.charges', string="Discount Charges", store=True) 

    odl_state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('first', "First Approval"),
            ('second', "Second Approval"),
            ('done', "Confirm"),
        ], string="ODL State", default='draft', required=True)

    # def discount_addition(self):
    #     for rec in self:
    #         discount_to_add = []
    #         product_in_line = [rec.line_ids.mapped('product_id.id')]
    #         installment_obj = [rec.line_ids[-1].mapped('installment_ids')]

    #         for discount in rec.discount_ids:
    #             if discount.product_id.id not in product_in_line:
    #                 discount_to_add.append(discount)

    #         for dis in discount_to_add:
    #             linedata={
    #                     'plan_id':self.ids[0],
    #                     'product_id':dis.product_id.id,
    #                     'name':dis.product_id.name,
    #                     'account_id':dis.product_id.property_account_income_id.id,
    #                     'quantity':1,
    #                     'installment_ids':[(6,0,[j.ids[0] for j in installment_obj])],
    #                     'currency_id':rec.currency_id.id,
    #                     'unit_price':0,
    #                     'discount_charges':True
    #                     }
    #             new_plan_line_id=rec.env['tuition.plan.line'].sudo().create(linedata)

    # def discount_remove(self):
    #     for rec in self:
    #         discount_to_remove = []
    #         # raise UserError(rec.discount_ids.mapped('product_id'))
    #         for line in rec.line_ids:

    #             if line.discount_charges and line.product_id.id not in rec.discount_ids.mapped('product_id.id'):
    #                 # raise UserError([line,"--",rec.discount_ids.mapped('product_id.id')])
    #                 line.unlink()

    def odl_first_approval(self):
        self.write({'odl_state': 'first'})

    def odl_second_approval(self):
        self.write({'odl_state': 'second'})

    def odl_confirm(self): 
        self.write({'odl_state': 'done'})


    
    # process end 

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
        self.write({'odl_state': 'draft'})

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
        #logic start
        
        if (plan.journal_id.name == 'Monthly Bills' or plan.journal_id.name == 'Bi Monthly') and len(plan.student_id.concession_line_ids) > 0:
            
            plan.update_line_concession()

        
        return plan

    def update_line_concession(self):
        for plan in self:
            installment_obj = plan.line_ids[-1].installment_ids
            

            line_concession_list = plan.student_id.concession_line_ids.get_concession_values(installment_obj)
            line_concession_list = [Command.create(vals) for vals in line_concession_list]

            # raise UserError(str(line_concession_list))
            
            plan.write({'line_ids': line_concession_list})

            # raise UserError(str(plan.line_ids))
            
    #logic end

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

# tuition.template.installment 

class TuitionTemplateInstallment(models.Model):
    _name = "tuition.template.installment"
    _inherit = 'tuition.installment.mixin'
    _description = "Tuition Plan Installment"

    tuition_template_id = fields.Many2one("tuition.template", "Tuition template", required=True, ondelete="cascade")

    lines_ids = fields.Many2many(
        'tuition.template.line',
        relation='tuition_template_installment_template_line_rel',
        column1='installment_id',
        column2='line_id',
        string="Lines")

    def get_installment_values(self):
        values = [
            {
                'name': installment.name,
                'sequence': installment.sequence,
                'type': installment.type,
                'day_type': installment.day_type,
                'day_of_the_month': installment.day_of_the_month,
                'month': installment.month,
                'date': installment.date,
                'template_installment_id': installment.id,
                'quarter': installment.quarter,
                } for installment in self]
        return values

    # def _get_monthly_date(self):
    #     self.ensure_one()
    #     if not self.month:
    #         return False
    #     today = fields.Date.today()
    #     if self.day_type == 'last_day':
    #         day = 31
    #     elif self.day_type == 'day_number':
    #         day = int(self.day_of_the_month)
    #     else:
    #         day = 1
    #     next_date = today + relativedelta(month=int(self.month), day=day)
    #     next_date = self.move_next_year_if_needed(next_date)
    #     return next_date

    def get_previous_installment(self):
        sorted_sibling_installments = self.tuition_template_id.installment_ids.sorted('sequence')
        previous_installment = self.browse()
        for i, installment in enumerate(sorted_sibling_installments):
            if i == 0 and installment == self:
                break
            elif installment == self:
                previous_installment = sorted_sibling_installments[i - 1]
        return previous_installment

    def get_next_installment(self):
        sorted_sibling_installments = self.tuition_template_id.installment_ids.sorted('sequence', reverse=True)
        next_installment = self.browse()
        for i, installment in enumerate(sorted_sibling_installments):
            if i == 0 and installment == self:
                break
            elif installment == self:
                next_installment = sorted_sibling_installments[i - 1]
        return next_installment

    def get_parent(self):
        self.ensure_one()
        return self.tuition_template_id

# tuition.template.line 

class TuitionPlanTemplateLine(models.Model):
    _name = 'tuition.template.line'
    _inherit = 'tuition.line.mixin'
    _description = "Tuition template line"

    template_id = fields.Many2one('tuition.template', required=True, ondelete='cascade')
    template_installment_ids = fields.One2many('tuition.template.installment', related='template_id.installment_ids')
    installment_ids = fields.Many2many(
        'tuition.template.installment',
        relation='tuition_template_installment_template_line_rel',
        column1='line_id',
        column2='installment_id',
        string="Installments",
        domain="[('id', 'in', template_installment_ids)]")
    company_id = fields.Many2one('res.company', related='template_id.company_id')

    # Analytic
    grade_level_ids = fields.Many2many('school.grade.level', string="Grade levels")
    domain = fields.Char(string="Domain", default="[]", required=True)

    @api.constrains('installment_ids')
    def _constraint_installment_ids(self):
        for line in self:
            for installment in line.installment_ids:
                if installment.tuition_template_id not in line.template_id:
                    raise ValidationError(_("A line has an installment from other template!"))

    @api.onchange('product_id')
    def onchange_product_id(self):
        for line in self:
            # if not line.product_id or line.display_type in ('line_section', 'line_note'):
            #     continue
            line.name = line._get_computed_name()
            taxes = line._get_computed_taxes()
            if taxes and line.template_id.fiscal_position_id:
                taxes = line.template_id.fiscal_position_id.map_tax(taxes)
            line.tax_ids = taxes
            line.product_uom_id = line._get_computed_uom()
            line.unit_price = line._get_computed_price_unit()
            line.account_id = line._get_computed_account()

    def get_tuition_plan_values(self, student):
        values = []

        for line in self:
            if line.should_apply_to_student(student):
                values.append({
                    'sequence': line.sequence,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'quantity': line.quantity,
                    'journal_id': line.journal_id.id,
                    'currency_id': line.currency_id.id,
                    'unit_price': line.unit_price,
                    'template_line_id': line.id,
                    'account_id': line.account_id.id,
                    'tax_ids': [Command.set(line.tax_ids.ids)],
                    'analytic_account_id': line.analytic_account_id.id,
                    'analytic_tag_ids': [Command.set(line.analytic_tag_ids.ids)],
                    'discount': line.discount,
                })
        return values

    def should_apply_to_student(self, student):
        enroll_status = student.get_enroll_status_line(program_id=self.template_id.program_id.id)
        domain = safe_eval(self.domain)
        if not student.filtered_domain(domain):
            return False
        if not self.grade_level_ids:
            return True
        return enroll_status.grade_level_id in self.grade_level_ids and enroll_status.enrollment_status_id.type == 'enrolled'

    def _get_computed_name(self):
        self.ensure_one()

        if self.env.lang:
            product = self.product_id.with_context(lang=self.env.lang)
        else:
            product = self.product_id

        values = []
        if product.partner_ref:
            values.append(product.partner_ref)
        if self.journal_id.type == 'sale':
            if product.description_sale:
                values.append(product.description_sale)
        return '\n'.join(values)

    def _get_computed_taxes(self):
        self.ensure_one()
        # Out invoice.
        if self.product_id.taxes_id:
            tax_ids = self.product_id.taxes_id.filtered(lambda tax: tax.company_id == self.template_id.company_id)
        elif self.account_id.tax_ids:
            tax_ids = self.account_id.tax_ids
        else:
            tax_ids = self.env['account.tax']
        if not tax_ids:
            tax_ids = self.template_id.company_id.account_sale_tax_id
        if self.company_id and tax_ids:
            tax_ids = tax_ids.filtered(lambda tax: tax.company_id == self.company_id)
        return tax_ids

    def _get_computed_account(self):
        self.ensure_one()
        self = self.with_company(self.template_id.journal_id.company_id)

        if not self.product_id:
            return

        fiscal_position = self.template_id.fiscal_position_id
        accounts = self.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
        return accounts['income'] or self.account_id

    def _get_computed_uom(self):
        self.ensure_one()
        if self.product_id:
            return self.product_id.uom_id
        return False

    def _get_computed_price_unit(self):
        self.ensure_one()

        if not self.product_id:
            return 0.0

        company = self.template_id.company_id
        currency = self.template_id.currency_id
        company_currency = company.currency_id
        product_uom = self.product_id.uom_id
        fiscal_position = self.template_id.fiscal_position_id
        move_date = fields.Date.context_today(self)

        product_price_unit = self.product_id.lst_price
        product_taxes = self.product_id.taxes_id.filtered(lambda tax: tax.company_id == company)

        # Apply unit of measure.
        if self.product_uom_id and self.product_uom_id != product_uom:
            product_price_unit = product_uom._compute_price(product_price_unit, self.product_uom_id)

        # Apply fiscal position.
        if product_taxes and fiscal_position:
            product_taxes_after_fp = fiscal_position.map_tax(product_taxes)

            if set(product_taxes.ids) != set(product_taxes_after_fp.ids):
                flattened_taxes_before_fp = product_taxes._origin.flatten_taxes_hierarchy()
                if any(tax.price_include for tax in flattened_taxes_before_fp):
                    taxes_res = flattened_taxes_before_fp.compute_all(
                        product_price_unit,
                        quantity=1.0,
                        currency=company_currency,
                        product=self.product_id,
                        is_refund=False,
                    )
                    product_price_unit = company_currency.round(taxes_res['total_excluded'])

                flattened_taxes_after_fp = product_taxes_after_fp._origin.flatten_taxes_hierarchy()
                if any(tax.price_include for tax in flattened_taxes_after_fp):
                    taxes_res = flattened_taxes_after_fp.compute_all(
                        product_price_unit,
                        quantity=1.0,
                        currency=company_currency,
                        product=self.product_id,
                        is_refund=False,
                        handle_price_include=False,
                    )
                    for tax_res in taxes_res['taxes']:
                        tax = self.env['account.tax'].browse(tax_res['id'])
                        if tax.price_include:
                            product_price_unit += tax_res['amount']

        # Apply currency rate.
        if currency and currency != company_currency:
            product_price_unit = company_currency._convert(product_price_unit, currency, company, move_date)

        return product_price_unit

# tuition.template 

class TuitionTemplate(models.Model):
    _name = 'tuition.template'
    _description = 'Tuition template'
    _inherit = 'tuition.plan.mixin'

    active = fields.Boolean(default=True)
    line_ids = fields.One2many('tuition.template.line', 'template_id')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
    installment_ids = fields.One2many('tuition.template.installment', 'tuition_template_id', string="Installments")
    tuition_plan_ids = fields.One2many('tuition.plan', 'tuition_template_id', string="Tuition plans")
    tuition_plan_count = fields.Integer(string="Tuition plan count", compute='compute_tuition_plan_count')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_approval', 'In Approval'),
        ('posted', 'Posted')
    ], string='State')
    installment_template = fields.Selection(selection=[
        ('quarterly', "Quarterly"),
        ('biannually', "Bi-Annually"),
        ('monthly', "Monthly"),
        ('yearly', "Yearly"),
        ], default='quarterly', string="Installment template")

    @api.onchange('program_id')
    def onchange_program_id(self):
        self.line_ids.grade_level_ids = False

    @api.onchange('installment_template')
    def onchange_installment_template(self):
        self.ensure_one()
        self.line_ids.installment_ids = False
        if self.installment_template == 'quarterly':
            self.set_quarterly_installment()
        elif self.installment_template == 'monthly':
            self.set_monthly_installment()
        elif self.installment_template == 'biannually':
            self.set_biannually_installment()
        elif self.installment_template == 'yearly':
            self.set_yearly_installment()

    @api.depends('tuition_plan_ids')
    def compute_tuition_plan_count(self):
        for template in self:
            template.tuition_plan_count = len(template.tuition_plan_ids)

    def button_new_tuition_plan(self):
        context = {'take_tuition_template_values': True, 'default_tuition_template_id': self.id}
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'create.bulk.tuition.plan',
            'view_mode': 'form',
            'target': 'new',
            'context': context
            }

    def _kanban_dashboard_graph(self):
        for template in self:
            template.kanban_dashboard_graph = json.dumps(template.get_bar_graph_datas())

    def get_bar_graph_datas(self):
        self.ensure_one()
        today = fields.Datetime.now(self)

        all_months = [datetime(today.year, month, 1) for month in range(1, 13)]
        labels = [format_date(month, 'MMMM', locale=get_lang(self.env).code) for month in all_months]
        return [{
            'labels': labels,
            'values': [{
                'label': "Income",
                'values': [random.randint(i, i*10) for i in range(0, 12)],
                'type': 'income',
                }, {
                'label': "Due",
                'values': [random.randint(i, i*10) for i in range(0, 12)],
                'type': 'due',
                }]
            }]

    def action_view_tuition_plans(self):
        self.ensure_one()
        tuition_plans = self.tuition_plan_ids
        action = self.env['ir.actions.actions']._for_xml_id('ol_school_account.tuition_plan_action')
        if len(tuition_plans) > 1:
            action['domain'] = [('id', 'in', tuition_plans.ids)]
        elif len(tuition_plans) == 1:
            form_view = [(self.env.ref('ol_school_account.tuition_plan_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = tuition_plans.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        if len(self) == 1:
            context = {
                'default_tuition_template_id': self.id,
                }
            action['context'] = context
        return action

    def set_quarterly_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q1',
                    'month': '9',
                    'day_type': 'first_day',
                    'sequence': 1
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q2',
                    'month': '12',
                    'day_type': 'first_day',
                    'sequence': 2
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q3',
                    'month': '3',
                    'day_type': 'first_day',
                    'sequence': 3
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q4',
                    'month': '6',
                    'day_type': 'first_day',
                    'sequence': 4
                    }),
                ]

    def set_monthly_installment(self):
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'monthly',
                    'month': '1',
                    'day_type': 'first_day',
                    'sequence': 1,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '2',
                    'day_type': 'first_day',
                    'sequence': 2,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '3',
                    'day_type': 'first_day',
                    'sequence': 3,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '4',
                    'day_type': 'first_day',
                    'sequence': 4,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '5',
                    'day_type': 'first_day',
                    'sequence': 5,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '6',
                    'day_type': 'first_day',
                    'sequence': 6,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '7',
                    'day_type': 'first_day',
                    'sequence': 7,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '8',
                    'day_type': 'first_day',
                    'sequence': 8,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '9',
                    'day_type': 'first_day',
                    'sequence': 9,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '10',
                    'day_type': 'first_day',
                    'sequence': 10,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '11',
                    'day_type': 'first_day',
                    'sequence': 11,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '12',
                    'day_type': 'first_day',
                    'sequence': 12,
                    }),
                ]

    def set_biannually_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'biannually',
                    'month': '9',
                    'sequence': 1,
                    }),
                Command.create({
                    'type': 'biannually',
                    'month': '1',
                    'sequence': 2,
                    }),
                ]

    def set_yearly_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'yearly',
                    'month': '1',
                    'day_type': 'first_day',
                    'sequence': 1,
                    }),
                ]

