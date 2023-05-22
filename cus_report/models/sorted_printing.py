from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import http
from odoo.http import request
from datetime import datetime 

class Sorted_cl(models.Model):
    _inherit = 'account.move'

    # challan_date = fields.Date(string='Challan Date')
    # x_studio_current_branchschool = fields.Many2one('your.branch.model', string='Branch')
    # class_name = fields.Many2one('your.class.model', string='Class')
    # section_name = fields.Many2one('your.section.model', string='Section')

    
    def get_sorted_records(self):
        records = self.search([])
        sorted_records = sorted(records, key=lambda x: (x.challan_date, x.x_studio_current_branchschool.name))
        raise UserError(sorted_records)
        #return sorted_records

    # def generate_report(self):
    #     records = self.search([])

    #     # Sort the records
    #     sorted_records = self.get_sorted_records(records)

    #     # Pass the sorted records to the report generation method
    #     report = env.ref('cus_report.fee_challan_student_wise').render_qweb_pdf(sorted_records)
    #      # Do further processing or return the report as needed