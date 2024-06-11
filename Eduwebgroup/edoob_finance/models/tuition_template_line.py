# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.fields import Command
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError


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
