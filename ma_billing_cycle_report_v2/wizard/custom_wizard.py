
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



class AccountMoveReport(models.TransientModel):
    _name = 'billing.student.report.line'
    
    record_id=fields.Char('ID')
    branch_name=fields.Char('name')
    # school_bill_len =fields.Float('Total')
    # billing_list_paid =fields.Float('Paid')

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
    
    account_report_line=fields.Many2many('billing.student.report.line', string='Account report Line')
    # by_account_report_line=fields.Many2many('student.bi.monthly.report.line', string='Account by Monthly report Line')
    
    def action_print_report(self):
        school_ids= []
        lines=[]
        school_ids_raw=self.env['school.school'].search([])
        school_ids_raw = school_ids_raw.sorted(lambda o : o.name)

        # v_from_month=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%m')
        # v_from_year=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y')

        # v_to_month=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%m')
        # v_to_year=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%y')

        # pay_from_month=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%m')
        # pay_from_year=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%y')

        # pay_to_month=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%m')
        # pay_to_year=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%y')

        for rec in school_ids_raw:
            if rec.name !="Milestone Model Town (Matric)":
            #     continue
                school_ids.append(rec)
            # raise UserError(rec) Milestone Model Town (Matric) or Milestone Model Town Senior Campus
           
            school_bill_ids = self.env['account.move'].search([
                ('x_studio_previous_branch', '=', rec.name),
                ('move_type','=','out_invoice'),
               ('invoice_date',">=",self.from_date),('invoice_date',"<=",self.to_date)
            ])


            # for bill_rec in school_bill_ids:



        for item in range(len(school_ids)):
            name_view = school_ids[item].name
            # billing_view = billing_list[name_view]
            # billing_paid_view = billing_list_paid[name_view]
            mvl=self.env['billing.student.report.line'].create({
                                        
                "branch_name":name_view,
                # "school_bill_len":billing_view,
                # "billing_list_paid":billing_paid_view,
            })
            lines.append(mvl.id)
        
        self.write({
            "account_report_line":[(6,0,lines)]
        })  


    def action_print_excel_billing_report(self):
        
        self.action_print_report()

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

            worksheet.write_merge(0,1,0,0, 'S#',  style=red_style_title)
            worksheet.write_merge(0,1,1,3, 'Branch',  style=red_style_title)
            worksheet.write_merge(0,1,4,6, 'Total Issuance',  style=red_style_title)
            worksheet.write_merge(0,1,7,9, 'Net Billing Exc.Withdrawals',  style=red_style_title)
            worksheet.write_merge(0,1,10,12, 'Total Recovery',  style=red_style_title)
            worksheet.write_merge(0,1,13,15, 'Receivables',  style=red_style_title)
            worksheet.write_merge(0,1,16,17, 'Bade Dabts',  style=red_style_title)
            worksheet.write_merge(0,1,18,20, "'%'age of Recovery on Enrolled and Paid Bills",  style=red_style_title)
            worksheet.write_merge(0,1,21,23, "Actual Recovery '%'age",  style=red_style_title)
            # worksheet.(0,1,0,3,"",)

            # v_from_month=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%m')
            # v_from_year=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y')

            # v_to_month=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%m')
            # v_to_year=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%y')   
            row=2
            col=4
            for rec in self.account_report_line:
                if rec:
                    # Print row data
                    worksheet.write_merge(row,row,1,3,rec.branch_name, style=style_title)

                    row+=1


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
        