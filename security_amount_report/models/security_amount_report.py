# import datetime
# from re import U

from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import http
from odoo.http import request
from datetime import datetime 


class SecurityAmountReport(models.Model):
    _name = "security.amount.report"

                
               

# For Excel Report Download Button 
class sale_day_book_report_excel(models.TransientModel):
    _name = "sale.day.book.report.excel"
    _description = "Sale Day Book Report Excel"
    
    
    excel_file = fields.Binary('Excel Report For Security Amount')
    file_name = fields.Char('Excel File', size=64)


