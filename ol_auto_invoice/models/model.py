
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from datetime import datetime
class ext(models.Model):
    _inherit="account.move"
    def create_auto_invoices(self):
        todaydate=datetime.now().date()
        students= self.env['school.student'].search([('enrolement_status_ids.name','in',['Enrolled'])])
        tuition_plans=self.env["tuition.plan"].search([('student_id','in',students.ids),('journal_id.name','in',["Monthly Bills"])])
        installments=self.env["tuition.installment"].search([("tuition_plan_id","in",tuition_plans.ids),("x_inv_date",'=',todaydate)])
        for installment in installments:
            tuition_plan = installment.tuition_plan_id
            tuition_plan.button_create_charge()
        return
        