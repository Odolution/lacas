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
            style_title = xlwt.easyxf(
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")

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

            
            # account_move_object = self.env['account.move'].search([])
            # domain = [('move_type', '=', 'out_refund')]
            # searching with filter that move_type is of out_refund type which is of Reversal
            # account_move_object = self.env['account.move'].search(domain)
            
            row = 1
            serial_number = 1
            enrolled_students = self.env['school.student'].search([('enrollment_status_ids.id','=', 2)])
            # raise UserError(enrolled_students)
            for student in enrolled_students:
                admission = self.env['account.move'].search([("move_type","=","out_invoice"),('journal_id.name','=','Admission Challan'), ("std_factsid","=",student.facts_id)], limit=1)
                reversal = self.env['account.move'].search([("move_type","=","out_refund"),('journal_id.name','=','Security Deposit'), ('state','=','posted'),("std_factsid","=",student.facts_id)], limit=1)
                for line in admission.invoice_line_ids:
                    if line.product_id.name == "Security":
                        worksheet.write(row, 0, serial_number)

                        if student.name:
                            worksheet.write(row, 1, student.name)
                        else:
                            worksheet.write(row, 1, "N/A")

                        if admission.partner_id.name:
                            worksheet.write(row, 2, admission.partner_id.name)
                        else:
                            worksheet.write(row, 2, "N/A")

                        if student.facts_udid:
                            worksheet.write(row, 3, student.facts_udid)
                        else:
                            worksheet.write(row, 3, "N/A")
                        
                        if admission.class_name:
                            worksheet.write(row, 4, admission.class_name)
                        else:
                            worksheet.write(row, 4, "N/A")
                            
                        if admission.student_ids:
                            student = self.env['school.student'].search([('id','=',admission.student_ids.id)])
                            if student:
                                homeroom = student.homeroom
                                if homeroom != False:
                                    vals = homeroom.split('-')
                                    if vals[-1].isalpha():
                                        worksheet.write(row, 5, vals[-1])
                                    else:
                                        student = self.env['school.student'].search([('id','=',reversal.student_ids.id)])
                                        if student:
                                            homeroom = student.homeroom
                                            if homeroom != False:
                                                vals = homeroom.split('-')
                                                if vals[-1].isalpha():
                                                    worksheet.write(row, 5, vals[-1])
                                                else:
                                                    worksheet.write(row, 5, "N/A")
                        else:
                            worksheet.write(row, 5, "N/A")

                        if student.x_last_school_id:
                            worksheet.write(row, 6, student.x_last_school_id.name)
                        else:
                            lst=str(student)
                            raise UserError(lst)
                            worksheet.write(row, 6, "N/A")

                        if admission.x_studio_withdrawn_status:
                            worksheet.write(row, 7, admission.x_studio_withdrawn_status)
                            
                        elif reversal.x_studio_withdrawn_status:
                            worksheet.write(row, 7, reversal.x_studio_withdrawn_status)
                            
                        else:
                            worksheet.write(row, 7, "N/A")

                        if admission.invoice_date:
                            worksheet.write(row, 8, str(admission.invoice_date))
                        else:
                            worksheet.write(row, 8, "N/A")
                         
                        if line.product_id.name == "Security":
                            worksheet.write(row, 9, line.price_total)
                        elif line.product_id.name != "Security":
                            for rev_line in reversal.invoice_line_ids:
                                if rev_line.name == 'Security':
                                    worksheet.write(row, 9, rev_line.price_total)
                                else:
                                    worksheet.write(row, 9, "N/A")
                        else:
                            worksheet.write(row, 9, "N/A")

                        serial_number += 1
                        row+=1
                    else:
                        pass
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
        

                
        
        # raise UserError(record_set) # It will print IDs of all the records.
    
        # raise UserError(record_set)
    

                
               

# For Excel Report Download Button 
class sale_day_book_report_excel(models.TransientModel):
    _name = "sale.day.book.report.excel"
    _description = "Sale Day Book Report Excel"
    
    
    excel_file = fields.Binary('Excel Report For Security Amount')
    file_name = fields.Char('Excel File', size=64)
