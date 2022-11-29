
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime

class custom_discount_model(models.Model):
    _name = "product.cdiscount"
    product_id = fields.Many2one('product.product', string='Charge on')
    discount_type = fields.Selection([
        ('percentage', 'percentage'),
        ('fixed', 'fixed'),
    ], string='type')
    discount_value = fields.Float('Value')
    @api.onchange('discount_value',"discount_type")
    def _onchange_value(self):
        if self.discount_type=="percentage" and self.discount_value>100:
            raise UserError("percentage cannot be larger then 100")
        

class product_ext(models.Model):
    _inherit = "product.product"
    is_discount_type = fields.Boolean('is_discount_type')
    discount_ids = fields.Many2many('product.cdiscount', string='Discount')

class template_ext(models.Model):
    _inherit = "product.template"
    is_discount_type = fields.Boolean('is_discount_type')
    discount_ids = fields.Many2many('product.cdiscount', string='Discount')
class invoice_ext(models.Model):

    _inherit = "account.move"
    def applyDiscount(self):
        
        for rec in self:
            
            for line in rec.invoice_line_ids:
                if line.product_id.is_discount_type:
                    total_amount_discount=0
                    for discount in line.product_id.discount_ids:
                        discount_amount=0
                        for line1 in rec.invoice_line_ids:
                            if discount.product_id.id==line1.product_id.id:
                                if discount.discount_type=="percentage":
                                    discount_amount+=(discount.discount_value/100)*line1.quantity*line1.price_unit
                                else:
                                    discount_amount+=discount.discount_value*line1.quantity
                        total_amount_discount+=discount_amount
                    line.tax_ids=False
                    line.quantity=1
                    line.price_unit=(-1)*total_amount_discount
                                
