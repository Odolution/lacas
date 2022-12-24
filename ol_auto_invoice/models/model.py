from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from datetime import datetime
class ext(models.Model):
    _inherit="account.move"
    def create_auto_invoices(self):
        todaydate=datetime.now().date()
        enrolement_status = self.env['school.enrollment.status'].search([('name','=',"Enrolled")])
        enrollment_ids=[i.id for i  in enrolement_status]
        students= self.env['school.student'].search([('enrollment_status_ids','in',enrollment_ids)])
        journals = self.env['account.journal'].search([('name','=',"Monthly Bills")])
        journal_ids=[i.id for i  in journals]
        tuition_plans=self.env["tuition.plan"].search([('student_id','in',students.ids),('journal_id','in',journal_ids),('state','=','posted')])
        
        # installments=env["tuition.installment"].search([("tuition_plan_id","in",tuition_plans.ids),("x_inv_date",'=',todaydate)])

        for plan in tuition_plans:
            while plan.next_installment_id.x_inv_date==todaydate:
              plan.button_create_charge()
        return
