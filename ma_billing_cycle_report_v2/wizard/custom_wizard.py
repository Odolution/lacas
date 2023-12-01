
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
    
    def action_print_excel_billing_report(self):
        if xlwt:
            global billing_counts ,by_monthly_billing_counts,select_by_monthly_list
            
            filename = 'Percentage wise billing cycle summary report v2.xls'
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            
            style_title = xlwt.easyxf(
            " align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            red_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour tan;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            yellow_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour light_green;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            lime_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour lime;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")

            grand_heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;'
                              'font: colour black, bold True;')

            heading_style = xlwt.easyxf('align: vertical center,horiz center;')
            
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'dd/mm/yyyy'

            # worksheet.write_merge(0, 1, 0, 5,"LACAS SCHOOL NETWORK ",style=style_title)
            # worksheet.write_merge(0, 1, 6, 11, "RECEIVABLE OF WITHDRAWAL STUDENTS", style=style_title)
            worksheet = workbook.add_sheet('Students Branch Std')

            sheet.write(0,0, 'S#',  style=red_style_title)
            sheet.write(0,1, 'Branch',  style=red_style_title)
            # worksheet.write_merge(0,1,0,3,"",)

            v_from_month=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%m')
            v_from_year=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y')

            v_to_month=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%m')
            v_to_year=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%y')   






            fp = io.BytesIO()
            workbook.save(fp)

            export_id = self.env['sale.day.book.report.excel'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
            res = {
                    'view_mode': 'form',
                    'res_id': export_id.id,
                    'res_model': 'sale.day.book.report.excel',
                    'type': 'ir.actions.act_window',
                    'target':'new'
                }
            return res

            
        else:
            raise Warning (""" You Don't have xlwt library.\n Please install it by executing this command :  sudo pip3 install xlwt""")
        