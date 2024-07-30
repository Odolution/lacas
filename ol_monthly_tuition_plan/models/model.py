
from odoo import models, api, fields, _
from odoo.exceptions import UserError

class InheritTuitionPlan(models.Model):
    _inherit = "school.student"
    monthly_bill_check = fields.Char('Monthly bill', compute = '_compute_monthly_bill_check')
    monthly_bill_check_related = fields.Char('Monthly bill check')
    
    def _compute_monthly_bill_check(self):
        for rec in self:
            rec.monthly_bill_check ='None'
            rec.monthly_bill_check_related = 'None'
            if rec.tuition_plan_count > 0:
                if rec.tuition_plan_ids:
                    admission_plan_check = True
                    bills_check = False
                    for plan in rec.tuition_plan_ids:
                        if plan.journal_id.name == 'Admission Challan':
                            if plan.account_move_count > 0:
                                for inv in plan.account_move_ids:
                                    if inv.journal_id.name == 'Admission Challan' and inv.payment_state == 'paid':
                                        bills_check = True
                        else:
                            admission_plan_check = False
                            break
                    
                    if admission_plan_check:
                        if bills_check:
                            rec.monthly_bill_check ='Paid Admission Challan'
                    else:
                        rec.monthly_bill_check ='None'
            rec.monthly_bill_check_related = rec.monthly_bill_check
        
            


        
            



    
