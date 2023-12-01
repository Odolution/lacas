
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

import xlsxwriter
_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import calendar

import base64

import io
try:
    import xlwt
except ImportError:
    xlwt = None



# class AccountMoveReport(models.TransientModel):
#     _name = 'billing.student.report.line'
    
#     record_id=fields.Char('ID')
#     branch_name=fields.Char('name')
#     school_bill_len =fields.Float('Total')
#     billing_list_paid =fields.Float('Paid')

# class ByMonthlyAccountMoveReport(models.TransientModel): 
#     _name = 'billing.student.bi.monthly.report.line'

    
#     record_id=fields.Char('ID')
#     branch_name=fields.Char('name')
#     school_bill_len =fields.Float('Total')
#     billing_list_paid =fields.Float('Paid')
    

class RecoveryReportWizard(models.TransientModel):
    _name="billing.cycle.report.wizard"
    _description='billing cycle summary report Wizard'

    
    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    from_date_pay = fields.Date(string='From')
    to_date_pay = fields.Date(string='To')
    
    # account_report_line=fields.Many2many('billing.student.report.line', string='Account report Line')
    # by_account_report_line=fields.Many2many('student.bi.monthly.report.line', string='Account by Monthly report Line')
    
