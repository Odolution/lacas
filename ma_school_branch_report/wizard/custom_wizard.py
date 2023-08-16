
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

import xlsxwriter
_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


import base64

import io
try:
    import xlwt
except ImportError:
    xlwt = None




class RecoveryReportWizard(models.TransientModel):
    _name="school.branch.report.wizard"
    _description='Print Recovery Wizard'

    # selected_month= fields.Many2many('billing.month', string='Select Month')
    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    all_branch=fields.Boolean(string=" Select All Branches")
    one_branch=fields.Many2one('school.school', string= 'Select any one branch')