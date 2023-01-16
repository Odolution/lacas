
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime

class add_plan_line_wiz(models.TransientModel):
    _name='tuition.add_plan_line_wiz'
    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    product_ids = fields.Many2many('product.product', string='Products')
    installment_names=fields.Many2Many('tuition.installment_names',string="Billing Month")
    def apply(self):
            for plan in self.plan_ids:
                for product in self.product_ids:
                        installment_ids=self.env.search([
                                        ('name','in',[i.name for i in self.installment_names]),
                                        ('plan_id','=',plan.id)])
                        linedata={
                                    'plan_id':plan.id,
                                    'product_id':product.id,
                                    'quantity':1,
                                    'installment_ids':[(6,0,[i.id for i in installment_ids])]
                                    }
                        new_plan_line_id=self.env['tuition.plan.line'].create(linedata)    
                    
    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        ids=self._context.get("active_ids")
        res["plan_ids"]=[(6,0,ids)]
        return res
class installment_names(models.Model):

    _name = "tuition.installment_names"
    name = fields.Char(string='Name')
#     def action_open_edit_installment_wiz(self):

#         return {
#             'name': _('Edit Installment'),
#             'res_model': 'tuition.edit_installment_wiz',
#             'view_mode': 'form',
#             'context': {
#                 'active_model': 'tuition.plan',
#                 'active_ids': self.ids,
#             },
#             'target': 'new',
#             'type': 'ir.actions.act_window',
#         }
