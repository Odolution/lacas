
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime



class add_plan_line_wiz(models.TransientModel):
    _name='tuition.add_plan_line_wiz'
    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    product_ids = fields.Many2many('product.product', string='Products')
    installment_names=fields.Many2many('installment.name',string="Billing Month")
    def apply(self):
            for plan in self.plan_ids:
                for product in self.product_ids:
                        installment_ids=self.env['tuition.installment'].search([
                                        ('name','in',[i.name for i in self.installment_names]),
                                        ('tuition_plan_id','=',plan.id)])
                        
                        linedata={
                                    'plan_id':plan.id,
                                    'product_id':product.id,
                                    'name':product.name,
                                    'account_id':product.property_account_income_id.id,
                                    'quantity':1,
                                    'installment_ids':[(6,0,[i.id for i in installment_ids])],
                                    'currency_id':product.currency_id.id,
                                    'unit_price':product.lst_price
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
