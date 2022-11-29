
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
                    # calculate total discount for this custom discount item
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
                    
                    ## add the discount to the invouce 

                    if total_amount_discount>0:
                        ##changing invoice line ids 
                        data={
                            "tax_ids":False,
                            "quantity":1,
                            "price_unit":(-1)*total_amount_discount
                        }
                        line.with_context(check_move_validity=False).write(data)

                        ## changing the journal lines
                        discount_line=False
                        recievable_line=False
                        for jl in rec.line_ids:
                            if jl.account_id.name=="Receivable from Customers":
                                recievable_line=jl
                            if jl.account_id.name=="Discount":
                                discount_line=jl
                        discount_line.with_context(check_move_validity=False).write({"debit":total_amount_discount,"credit":0})
                        recievable_line.with_context(check_move_validity=False).write({"debit":recievable_line.debit-total_amount_discount,"credit":0})

