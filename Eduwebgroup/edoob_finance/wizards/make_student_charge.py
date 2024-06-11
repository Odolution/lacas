# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.fields import Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare


class MakeStudentCharge(models.TransientModel):
    _name = 'make.student.charge'
    _description = 'Make charge for an student'

    @api.model
    def _get_default_journal(self):
        return self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()

    @api.model
    def _default_pricelist_id(self):
        return self.env['product.pricelist'].search(['|', ('company_id', '=', False), ('company_id', '=', self.env.company.id)], limit=1)

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        ctx = self._context
        if 'active_ids' in ctx:
            students = ctx.get('active_ids', [])
        else:
            students = [ctx.get('active_id')] if 'active_id' in ctx else []
        if students:
            defaults['student_ids'] = [Command.set(students)]
        return defaults

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    student_ids = fields.Many2many('school.student', required=True)
    line_ids = fields.One2many('make.student.charge.line', 'wizard_id', required=True)
    tax_country_id = fields.Many2one(
        'res.country', compute='_compute_tax_country_id',
        help='Technical field to filter the available taxes depending on the fiscal country and fiscal position.')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    journal_id = fields.Many2one('account.journal', string="Default journal", domain="[('type', '=', 'sale')]")
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic account')
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment terms', check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    pricelist_option = fields.Selection(
        selection=[
            ('fixed_prices', "Fixed prices"),
            ('invoice_address', "Invoice address"),
            ('student', "Student"),
            ('fixed_pricelist', "Fixed pricelist"),
        ], default='fixed_prices', required=True)
    pricelist_id = fields.Many2one('product.pricelist', default=_default_pricelist_id)

    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position',
        domain="[('company_id', '=', company_id)]", check_company=True,
        help='Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices.'
             'The default value comes from the customer.')
    split_by_student = fields.Boolean(
        string='Split by student', default=lambda self: self.env.company.edoob_finance_split_by_student)

    mode = fields.Selection(selection=[
        ('sale', 'Sale order'),
        ('move', 'Invoice'),
        ], default='sale', required=True)
    post_action_option = fields.Selection(selection=[
        ('nothing', "Do nothing"),
        ('send', "Send"),
        ('confirm', "Confirm"),
        ('confirm_send', "Confirm & send"),
        ], default='confirm_send', required=True, string="Post-action option")

    mail_template_id = fields.Many2one('mail.template', 'Mail Template', domain=[('model', 'in', ('sale.order', 'account.move'))])

    @api.onchange('post_action_option', 'mode')
    def onchange_post_action_option(self):
        if self.post_action_option in ('send', 'confirm_send'):
            if self.mode == 'sale':
                default_template_id = self.env['ir.model.data']._xmlid_to_res_id('sale.email_template_edi_sale', raise_if_not_found=False)
                self.mail_template_id = default_template_id
            if self.mode == 'move':
                default_template_id = self.env['ir.model.data']._xmlid_to_res_id("account.email_template_edi_invoice", raise_if_not_found=False)
                self.mail_template_id = default_template_id

    @api.constrains('mode', 'post_action_option')
    def check_invoice_should_be_posted_before_sent(self):
        for record in self:
            if record.mode == 'move' and record.post_action_option == 'send':
                raise UserError(_("You cannot use the post-action option 'send' if you are using the invoice mode.\nInvoices should be posted before being sent."))

    @api.onchange('mode')
    def onchange_mode(self):
        if self.mode == 'move':
            self.journal_id = self._get_default_journal()
            if self.post_action_option == 'send':
                self.post_action_option = 'confirm_send'

    @api.onchange('journal_id')
    def onchange_journal_id(self):
        self.line_ids.journal_id = self.journal_id

    @api.depends('company_id.account_fiscal_country_id', 'fiscal_position_id.country_id', 'fiscal_position_id.foreign_vat')
    def _compute_tax_country_id(self):
        for record in self:
            if record.fiscal_position_id.foreign_vat:
                record.tax_country_id = record.fiscal_position_id.country_id
            else:
                record.tax_country_id = record.company_id.account_fiscal_country_id

    def button_confirm(self):
        records = None
        if self.split_by_student:
            for student in self.student_ids:
                if records is None:
                    records = self._make_charge(student)
                else:
                    records += self._make_charge(student)
        else:
            records = self._make_charge(self.student_ids)
        return self._go_to_records(records)

    def _make_charge(self, students):
        self.ensure_one()
        if self.mode == 'sale':
            sale_vals = self._prepare_sale_order_values(students)
            sales = self.env['sale.order'].create(sale_vals)
            self._do_post_action(sales)
            return sales
        if self.mode == 'move':
            move_vals = self._prepare_account_move_values(students)
            moves = self.env['account.move'].create(move_vals)
            self._do_post_action(moves)
            return moves

    def _prepare_sale_order_values(self, students):
        families = students.family_ids
        students_by_families = [(family, students.filtered(lambda s: family in s.family_ids)) for family in families]
        # todo: partner_pricelist = plan.pricelist_id
        invoice_date = fields.Date.today()
        # sale_pricelist = partner_pricelist
        journals = self.line_ids.mapped('journal_id')
        lines_by_journal = [(journal, self.line_ids.filtered(lambda l: l.journal_id == journal)) for journal in journals] or [(journals, self.line_ids)]
        sale_vals_list = []

        for journal, lines in lines_by_journal:
            for family, family_students in students_by_families:
                if not family.invoice_address_id:
                    raise UserError(_("Family %s[%s] doesn't have an invoice address!", family.name, family.id))
                sale_values = self._prepare_sale_order_values_for_family(family, family_students, lines, invoice_date, journal)
                if sale_values:
                    sale_vals_list.append(sale_values)
        return sale_vals_list


    def _prepare_sale_order_values_for_family(self, family, family_students, lines, invoice_date, journal):
        order_line_vals = []
        for student in family_students:
            for line in lines:
                line_vals = line.prepare_sale_order_values(student, family)
                if line_vals['price_unit']:
                    order_line_vals.append(Command.create(line_vals))
        if not order_line_vals:
            return False
        sale_values = {
                    'date_order': invoice_date,
                    'partner_id': family.invoice_address_id.id,
                    'family_id': family.id,
                    'analytic_account_id': self.analytic_account_id.id,
                    'order_line': order_line_vals,
                    'origin': "Make sale",
                    'payment_term_id': self.payment_term_id.id,
                    'pricelist_id': family.invoice_address_id.property_product_pricelist.id,
                    'company_id': self.company_id.id,
                    'edoob_finance_journal_id': journal.id,
                }
        return sale_values

    def _prepare_account_move_values(self, students):
        families = students.family_ids
        students_by_families = [(family, students.filtered(lambda s: family in s.family_ids)) for family in families]
        invoice_date = fields.Date.today()
        journals = self.line_ids.mapped('journal_id')
        lines_by_journal = [(journal, self.line_ids.filtered(lambda l: l.journal_id == journal)) for journal in journals] or [(journals, self.line_ids)]
        invoice_vals_list = []

        for journal, lines in lines_by_journal:
            for family, family_students in students_by_families:
                if not family.invoice_address_id:
                    raise UserError(_("Family %s[%s] doesn't have an invoice address!", family.name, family.id))
                invoice_vals = self._prepare_invoice_values_for_family(family, family_students, lines, invoice_date, journal)
                if invoice_vals:
                    invoice_vals_list.append(invoice_vals)
        return invoice_vals_list

    def _prepare_invoice_values_for_family(self, family, family_students, lines, invoice_date, journal):
        move_line_ids = []
        for student in family_students:
            for line in lines:
                line_vals = line.prepare_invoice_line_values(student, family)
                if line_vals['price_unit']:
                    move_line_ids.append(Command.create(line_vals))
        if not move_line_ids:
            return False
        invoice_values = {
            'invoice_date': invoice_date,
            'partner_id': family.invoice_address_id.id,
            'family_id': family.id,
            'invoice_line_ids': move_line_ids,
            'company_id': self.company_id.id,
            'journal_id': journal.id,
            'invoice_payment_term_id': self.payment_term_id.id,
            'move_type': 'out_invoice',
        }
        return invoice_values

    def _do_post_action(self, records):
        if self.post_action_option in ('confirm', 'confirm_send'):
            self._confirm_records(records)
        if self.post_action_option in ('send', 'confirm_send'):
            self.send_records(records)

    # noinspection PyMethodMayBeStatic
    def send_records(self, records):
        if records._name == 'sale.order':
            self._send_records(records, self.mail_template_id.id)
            for sale in records:
                if sale.state == 'draft':
                    records.action_quotation_sent()
        elif records._name == 'account.move':
            for move in records:
                self._send_records(move, self.mail_template_id.id)

    def _send_records(self, records, template_id):
        for record in records:
            composer = self.env['mail.compose.message'].with_context(
                active_id=record.id,
                active_ids=record.ids,
                active_model=records._name,
                default_composition_mode='comment',
                default_model=records._name,
                default_res_id=record.id,
                default_template_id=template_id,
                custom_layout='mail.mail_notification_paynow',
            ).create({})
            if template_id:
                update_values = composer._onchange_template_id(template_id, 'comment', records._name, record.id)['value']
                composer.write(update_values)
            recipients = record.student_ids.get_individual_invoice_recipients(family_id=record.family_id.id)
            if recipients:
                composer.write({'partner_ids': [Command.link(r.partner_id.id) for r in recipients]})
            composer._action_send_mail()

    # noinspection PyMethodMayBeStatic
    def _confirm_records(self, records):
        if records._name == 'sale.order':
            records.action_confirm()
        elif records._name == 'account.move':
            records.action_post()

    @api.model
    def _go_to_records(self, records):
        action_data = self._get_action_data_depending_on_model(records)
        if not action_data:
            return {'type': 'ir.actions.act_window_close'}
        action = action_data['action']
        additional_context = action_data.get('additional_context', {})
        form_view = action_data['form_view']

        if 'context' in action and type(action['context']) == dict:
            action['context'].update(additional_context)

        if len(records) > 1:
            action['domain'] = [('id', 'in', records.ids)]
        elif len(records) == 1:
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = records.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.model
    def _get_action_data_depending_on_model(self, records):
        if records._name == 'sale.order':
            return {
                'action':  self.env['ir.actions.actions']._for_xml_id('sale.action_quotations'),
                'additional_context': {},
                'form_view':  [(self.env.ref('sale.view_order_form').id, 'form')],
                }
        elif records._name == 'account.move':
            return {
                'action': self.env['ir.actions.actions']._for_xml_id('account.action_move_out_invoice_type'),
                'additional_context': {},
                'form_view': [(self.env.ref('account.view_move_form').id, 'form')],
                }
        else:
            return False

    def get_pricelist(self, student, family=False, *args, **kwargs):
        self.ensure_one()
        if self.pricelist_option == 'student':
            return student.property_product_pricelist
        elif self.pricelist_option == 'fixed_pricelist':
            return self.pricelist_id
        elif self.pricelist_option == 'invoice_address' and family:
            if not family.invoice_address_id:
                raise UserError(_("The family %s doesn't have a invoice address"))
            return family.invoice_address_id.property_product_pricelist
        return False


class MakeStudentChargeLine(models.TransientModel):
    _name = 'make.student.charge.line'
    _description = 'Make charge lines for an student'
    _order = 'sequence'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Description', required=True)
    wizard_id = fields.Many2one('make.student.charge', required=True, ondelete='cascade')

    company_id = fields.Many2one('res.company', string='Company', related='wizard_id.company_id')
    wizard_currency_id = fields.Many2one('res.company', string='Company', related='wizard_id.currency_id')

    product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='restrict')
    product_uom_id = fields.Many2one(
        'uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]",
        ondelete='restrict')
    product_uom_category_id = fields.Many2one('uom.category', related='product_id.uom_id.category_id')

    account_id = fields.Many2one(
        'account.account', string='Account',
        index=True, ondelete='cascade',
        domain="[('deprecated', '=', False), ('company_id', '=', 'company_id'),('is_off_balance', '=', False)]",
        check_company=True,
        tracking=True)
    journal_id = fields.Many2one('account.journal', string='Journal', domain="[('type', '=', 'sale')]")
    quantity = fields.Float('Quantity', default=1.0, digits='Product Unit of Measure')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    unit_price = fields.Monetary('Unit price')
    tax_ids = fields.Many2many('account.tax', string='Taxes')

    discount = fields.Float('Discount', digits='Discount', default=0.0)

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    # Analytic
    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account',
        index=True, compute_sudo='_compute_analytic_fields', store=True, readonly=False, check_company=True, copy=True)
    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag', string='Analytic Tags', compute_sudo='_compute_analytic_fields',
        store=True, readonly=False, check_company=True, copy=True)

    @api.depends('quantity', 'discount', 'unit_price', 'tax_ids')
    def _compute_amount(self):
        """ Compute the amounts of the SO line. """
        for line in self:
            price = line.unit_price * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.currency_id, line.quantity, product=line.product_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_ids.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_ids.id])

    @api.depends('product_id', 'account_id')
    def _compute_analytic_fields(self):
        for line in self:
            rec = self.env['account.analytic.default'].account_get(
                product_id=line.product_id.id,
                account_id=line.account_id.id,
                user_id=line.env.uid,
                date=fields.Date.today(),
                company_id=self.env.company.id,
            )
            line.analytic_account_id = rec.analytic_id
            line.analytic_tag_ids = rec.analytic_tag_ids

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            line.name = line._get_computed_name()
            taxes = line._get_computed_taxes()
            if taxes and line.wizard_id.fiscal_position_id:
                taxes = line.wizard_id.fiscal_position_id.map_tax(taxes)
            line.tax_ids = taxes
            line.product_uom_id = line._get_computed_uom()
            line.unit_price = line._get_computed_price_unit()
            line.account_id = line._get_computed_account()

    @api.onchange('company_id', 'wizard_currency_id')
    def _onchange_company_id(self):
        self.currency_id = self.company_id.currency_id
        for line in self:
            line.name = line._get_computed_name()
            taxes = line._get_computed_taxes()
            if taxes and line.wizard_id.fiscal_position_id:
                taxes = line.wizard_id.fiscal_position_id.map_tax(taxes)
            line.tax_ids = taxes
            line.product_uom_id = line._get_computed_uom()
            line.unit_price = line._get_computed_price_unit()

    def _get_computed_name(self):
        self.ensure_one()
        students = self.wizard_id.student_ids
        student = self.wizard_id.student_ids[:1]

        if len(students) == 1 and student.lang:
            product = self.product_id.with_context(lang=student.lang)
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
            tax_ids = self.product_id.taxes_id.filtered(lambda tax: tax.company_id == self.company_id)
        elif self.account_id.tax_ids:
            tax_ids = self.account_id.tax_ids
        else:
            tax_ids = self.env['account.tax']
        if not tax_ids:
            tax_ids = self.company_id.account_sale_tax_id
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
        self = self.with_company(self.wizard_id.journal_id.company_id)

        if not self.product_id:
            return

        fiscal_position = self.wizard_id.fiscal_position_id
        accounts = self.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
        return accounts['income'] or self.account_id

    def _get_computed_price_unit(self):
        company = self.company_id

        self.ensure_one()
        students = self.wizard_id.student_ids
        student = self.wizard_id.student_ids[:1]

        if not self.product_id:
            return 0.0

        company = self.company_id
        currency = self.currency_id
        company_currency = company.currency_id
        product_uom = self.product_id.uom_id
        fiscal_position = self.wizard_id.fiscal_position_id
        move_date = fields.Date.context_today(self)

        product_price_unit = self.product_id.lst_price
        product_taxes = self.product_id.taxes_id.filtered(lambda tax: tax.company_id == company)

        # Apply unit of measure.
        if self.product_uom_id and self.product_uom_id != product_uom:
            product_price_unit = product_uom._compute_price(product_price_unit, self.product_uom_id)

        # Apply fiscal position.
        if len(students) == 1 and product_taxes and fiscal_position:
            product_taxes_after_fp = fiscal_position.map_tax(product_taxes)

            if set(product_taxes.ids) != set(product_taxes_after_fp.ids):
                flattened_taxes_before_fp = product_taxes._origin.flatten_taxes_hierarchy()
                if any(tax.price_include for tax in flattened_taxes_before_fp):
                    taxes_res = flattened_taxes_before_fp.compute_all(
                        product_price_unit,
                        quantity=1.0,
                        currency=company_currency,
                        product=self.product_id,
                        partner=student,
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
                        partner=student,
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

    def prepare_sale_order_values(self, student, family=False, ):
        self.ensure_one()
        unit_price, discount = self._get_unit_price_and_discount(student, family)
        return {
            'sequence': self.sequence,
            'product_id': self.product_id.id,
            'name': self.name,
            'product_uom_qty': self.quantity,
            'price_unit': unit_price,
            'discount': discount,
            'tax_id': [Command.set(self.tax_ids.ids)],
            'student_id': student.id,
        }

    def prepare_invoice_line_values(self, student, family=False):
        self.ensure_one()
        unit_price, discount = self._get_unit_price_and_discount(student, family)
        return {
            'product_id': self.product_id.id,
            'account_id': self.account_id.id,
            'sequence': self.sequence,
            'name': self.name,
            'quantity': self.quantity,
            'product_uom_id': self.product_uom_id.id,
            'discount': discount,
            'price_unit': unit_price,
            'tax_ids': [Command.set(self.tax_ids.ids)],
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'student_id': student.id,
            'analytic_account_id': self.analytic_account_id.id,
            }

    def _get_unit_price_and_discount(self, student, family=False):
        if not family or self.wizard_id.pricelist_option == 'fixed_prices':
            return self.unit_price, self.discount
        pricelist_data = self._get_pricelist_data(student, family)
        unit_price = self._get_unit_price(student, pricelist_data['product_price'], family)
        return unit_price, pricelist_data['discount']

    def _get_unit_price(self, student, pricelist_price, family=False):
        parent_category_id = self.product_id.categ_id
        available_categories = student.mapped('financial_responsibility_ids.product_category_id')

        while parent_category_id:
            if parent_category_id in available_categories:
                break
            parent_category_id = parent_category_id.parent_id

        if not parent_category_id:
            raise UserError(_(
                "%s[%s] doesn't have a responsible family for %s", student.name, student.id, self.product_id.categ_id.complete_name))

        percentage_sum = sum([category.percentage for category in student.financial_responsibility_ids if
                              category.product_category_id == parent_category_id and category.family_id == family])
        return pricelist_price * percentage_sum

    def _get_pricelist_partner(self, student, family=False):
        """
        :return: False if there is no unique partner
        """
        if self.wizard_id.pricelist_option in ('student', 'fixed_pricelist', 'fixed_prices'):
            return student
        elif self.wizard_id.pricelist_option == 'invoice_address' and family:
            return family.invoice_address_id
        return False

    def _get_pricelist_data(self, student, family=False):
        if not family or self.wizard_id.pricelist_option == 'fixed_prices':
            return self.unit_price

        partner = self._get_pricelist_partner(student, family)
        pricelist = self.wizard_id.get_pricelist(student, family)

        product = self.product_id
        quantity = self.quantity
        product_uom = self.product_uom_id
        date = fields.Date.today()
        company = self.company_id
        return self.env['edoob.finance.util'].get_pricelist_price_data(pricelist, product, quantity, product_uom, partner, date, company)

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
