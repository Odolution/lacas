# import datetime
# from re import U

from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import http
from odoo.http import request
from datetime import datetime 
import io
import base64
import xlwt


class SecurityAmountReport(models.Model):
    _name = "security.amount.report"

    def print_xlsx(self):
        if xlwt:
            
            report_name = 'Security Amount Report'
            filename = 'Security Amount Report.xls'
            
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('Security Amount Report')
            column_width = 30 * 256
            style_title = xlwt.easyxf(
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin; f'width {column_width}'")

            grand_heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True;')

            heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour black;'
                              'font: colour white, bold True;')
            
            
            
            
            date_format = xlwt.XFStyle()
            
            # First two numbers are Rows, Last Two Numbers are Columns
            
            # worksheet.write_merge(6, 7, 5, 14, "SECURITY AMOUNT REPORT", style=style_title)

            field_names = ['Sr.#', 'STUDENT NAME', 'FATHER NAME', '6 DIGIT ID', 'CLASS', 'SECTION', 'BRANCH', 'WITHDRAWN', 'ADM. DATE', 'SECURITY']

            for col, field_name in enumerate(field_names):
                worksheet.write_merge(0, 0, col*1, col*1, field_name, style=style_title)

            unique_students={}
            journal_items=self.env['account.move.line'].search([('account_id.code','=','6612485')])
            for item in journal_items:
                students=item.move_id.student_ids
                for stu in students:
                    unique_students[stu.id]=item               


            # Step 4: Write the results in an Excel file
            row = 1
            serial_number = 1
            lst=[]
            for stu_id,item in unique_students.items():
                student_data=self.env['school.student'].search([('id','=',stu_id)])
                if item.debit != 0:
                    security_amount= item.debit
                else:
                    security_amount= item.credit
                worksheet.write(row, 0, serial_number)
                worksheet.write(row, 1, student_data.name if student_data.name else "N/A")
                worksheet.write(row, 2, item.partner_id.name if item.partner_id.name else "N/A")
                worksheet.write(row, 3, student_data.facts_udid if student_data.facts_udid else "N/A")

                # worksheet.write(row, 3, student_object.student_code if student_object.student_code else "N/A")
                # if student_object.student_code:
                #     worksheet.write(row, 3, student_object.student_code)
                # elif student_object.udid_cred_custom:
                #     worksheet.write(row, 3, student_object.udid_cred_custom)
                # else:
                #     worksheet.write(row, 3, "N/A")

                worksheet.write(row, 4, item.move_id.class_name if item.move_id.class_name else "N/A")
                worksheet.write(row, 5, item.move_id.section_name if item.move_id.section_name else "N/A")
                worksheet.write(row, 6, item.move_id.std_current_branch if item.move_id.std_current_branch else "N/A")
                
                # if student_object.std_current_branch:
                #     worksheet.write(row, 6, student_object.std_current_branch)
                # elif student_object.x_school_id_cred.name:
                #     worksheet.write(row, 6, student_object.x_school_id_cred.name)
                # else:
                #     worksheet.write(row, 6, "N/A")
                
                worksheet.write(row, 7, item.move_id.x_studio_withdrawn_status if item.move_id.x_studio_withdrawn_status else "N/A")
                worksheet.write(row, 8, str(item.move_id.invoice_date) if item.move_id.invoice_date else "N/A")
                worksheet.write(row, 9, security_amount if security_amount else "N/A")

                serial_number += 1
                row += 1

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
               

# For Excel Report Download Button 
class sale_day_book_report_excel(models.TransientModel):
    _name = "sale.day.book.report.excel"
    _description = "Sale Day Book Report Excel"
    
    
    excel_file = fields.Binary('Excel Report For Security Amount')
    file_name = fields.Char('Excel File', size=64)


