# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command


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

        pricelist_data = self.env['edoob.finance.util'].get_pricelist_price_data(
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
        percentage = self.env['edoob.finance.util']._get_family_percentage(self.plan_id.student_id, family, self.product_id)
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
        percentage = self.env['edoob.finance.util']._get_family_percentage(self.plan_id.student_id, family, self.product_id)
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
            'views': [(self.env.ref('edoob_finance.tuition_plan_family_prices_view_tree').id, 'list')],
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
            pricelist_data = self.env['edoob.finance.util'].get_pricelist_price_data(
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

                    pricelist_data = self.env['edoob.finance.util'].get_pricelist_price_data(
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

