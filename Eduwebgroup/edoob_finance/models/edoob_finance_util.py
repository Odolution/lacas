# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError
from odoo.fields import Command

import datetime
from dateutil.relativedelta import relativedelta


class EdoobFinanceUtil(models.AbstractModel):
    _name = 'edoob.finance.util'
    _description = "Edoob finance util"

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
