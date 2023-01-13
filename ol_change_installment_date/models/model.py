
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime

class edit_installment_wiz(models.TransientModel):
    _name='tuition.edit_installment_wiz'
    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    installment_month=fields.Char(string="Installment")
    month = fields.Char('Month')
    day = fields.Integer('Day')
    def apply(self):
        for wizard in self:
            for plan in wizard.plan_ids:
                pass

    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        ids=self._context.get("active_ids")
        res["plan_ids"]=[(6,0,ids)]
        return res

# class plan_ext(models.Model):

#     _inherit = "tuition.plan"
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
