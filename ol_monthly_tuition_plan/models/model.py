
from odoo import models, api, fields, _
from odoo.exceptions import UserError

class InheritTuitionPlan(models.Model):
    _inherit = "school.student"
    monthly_bill_check = fields.Char('Monthly bill check')
    
    def _compute_monthly_bill_check(self):
        for rec in self:
            pass



    
