from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import datetime

class ChallanPrinting(models.Model):
    _name = 'challan.printing'
    _description = 'Challan Printing'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    branch_ids = fields.Many2many('school.school', string='Branch')
    class_ids = fields.Many2many('school.grade.level', string='Class')
    journal_id = fields.Many2one('account.journal', string='Journal')
    enrollment_status_ids = fields.Many2many('school.enrollment.status', string='Enrollment Status')


    def generate_pdf_challan(self):
        pass