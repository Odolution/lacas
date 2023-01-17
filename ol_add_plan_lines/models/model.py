
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime



class add_plan_line_wiz(models.TransientModel):
    _name='tuition.add_plan_line_wiz'
    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    product_id = fields.Many2one('product.product', string='Product')
    installment_names=fields.Many2many('installment.name',string="Billing Cycle")
    
    unit_price=fields.Integer("Unit Price")
    currency_id=fields.Many2one('res.currency',"Currency")
    quantity = fields.Integer("Quantity")
    def apply(self):
            for plan in self.plan_ids:
                        names=[i.name for i in self.installment_names]
                        installment_ids=self.env['tuition.installment'].search([
                                        ('name','in',names),
                                        ('tuition_plan_id','=',plan.id)])
                        
                        linedata={
                                    'plan_id':plan.id,
                                    'product_id':self.product_id.id,
                                    'name':self.product_id.name,
                                    'account_id':self.product_id.property_account_income_id.id,
                                    'quantity':self.quantity,
                                    'installment_ids':[(6,0,[i.id for i in installment_ids if i.name in names])],
                                    'currency_id':self.currency_id.id,
                                    'unit_price':self.unit_price if self.unit_price>0 else product.lst_price
                                    }
                        new_plan_line_id=self.env['tuition.plan.line'].create(linedata)


    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        ids=self._context.get("active_ids")
        res["plan_ids"]=[(6,0,ids)]
        return res
class installment_names(models.Model):

    _name = "installment.name"
    name = fields.Char(string='Name')
