# -*- coding: utf-8 -*-

from odoo import fields, models, api


class TuitionPlanLineMixin(models.AbstractModel):
    _inherit = 'mail.thread'
    _name = 'tuition.line.mixin'
    _description = "Tuition line mixin"
    _order = 'sequence'

    sequence = fields.Integer("Sequence")
    name = fields.Char("Description", required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True, ondelete='restrict')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
    product_uom_category_id = fields.Many2one('uom.category', related='product_id.uom_id.category_id')

    account_id = fields.Many2one(
        'account.account', string='Account',
        index=True, ondelete="cascade",
        domain="[('deprecated', '=', False), ('company_id', '=', 'company_id'),('is_off_balance', '=', False)]",
        check_company=True,
        tracking=True)
    journal_id = fields.Many2one('account.journal', string="Journal", domain="[('type', '=', 'sale')]")
    quantity = fields.Float("Quantity", default=1.0, digits='Product Unit of Measure')
    currency_id = fields.Many2one('res.currency', string="Currency", required=True)
    unit_price = fields.Monetary("Unit price")
    tax_ids = fields.Many2many('account.tax', string="Taxes")

    discount = fields.Float("Discount", digits='Discount', default=0.0)

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)
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

    # def _get_display_price(self, product, partner, pricelist, date_order):
    #     # TO DO: move me in master/saas-16 on sale.order
    #     # awa: don't know if it's still the case since we need the "product_no_variant_attribute_value_ids" field now
    #     # to be able to compute the full price
    #
    #     # it is possible that a no_variant attribute is still in a variant if
    #     # the type of the attribute has been changed after creation.
    #     if pricelist.discount_policy == 'with_discount':
    #         return product.with_context(pricelist=pricelist.id, uom=self.product_uom_id.id).price
    #     product_context = dict(self.env.context, partner_id=partner.id, date=date_order, uom=self.product_uom_id.id)
    #
    #     final_price, rule_id = pricelist.with_context(product_context).get_product_price_rule(product or self.product_id, self.quantity or 1.0, partner)
    #     base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.quantity, self.product_uom, pricelist.id)
    #     if currency != pricelist.currency_id:
    #         base_price = currency._convert(
    #             base_price, pricelist.currency_id,
    #             self.order_id.company_id or self.env.company, date_order or fields.Date.today())
    #     # negative discounts (= surcharge) are included in the display price
    #     return max(base_price, final_price)
