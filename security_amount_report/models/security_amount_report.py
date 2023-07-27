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
            # start_date_string = str(self.custom_start_date)
            # end_date_string = str(self.custom_end_date) 
            # def format_date(date_string):
            #     date = datetime.strptime(date_string, '%Y-%m-%d')
            #     formatted_date = date.strftime('%m/%d/%Y')
            #     return formatted_date
            # formatted_start_date = format_date(start_date_string)
            # formatted_end_date = format_date(end_date_string)
            
            
            # names_of_employees = []
            # for value in self.employee_names:
                # names_of_employees.append(value.name)
            
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
            
            # raise UserError(self.custom_start_date)
            # worksheet.write_merge(0, 1, 0, 9,"ZUMA LIFT SERVICE INC. ",style=style_title)
            worksheet.write_merge(2, 3, 0, 9, "SECURITY AMOUNT REPORT", style=style_title)

            field_names = ['Sr.#', 'STUDENT NAME', 'FATHER NAME', '6 DIGIT ID', 'CLASS', 'CLASS', 'SECTION', 'BRANCH', 'WITHDRAWN', 'ADM. DATE', 'GENDER', 'SECURITY']

            for col, field_name in enumerate(field_names):
                worksheet.write_merge(10, 10, col*2, col*2+1, field_name, style=style_title)

            
            account_move_object = self.env['account.move'].search([])

            row = 7
            for record in account_move_object.student_ids:
                serial_number = 1
                worksheet.write_merge(row, row, 0, 1, serial_number)
            # for record in self.partner_id:
            #     serial_number+=1
            #     # Increment the column for each field
            #     col = 2
            #     employee_name = record.employee_id.name
            #     worksheet.write_merge(row, row, 0, 1, employee_name)
            #     # worksheet.write(row, col, record.custom_attendance_value)
            #     worksheet.write_merge(row, row, 2, 3, record.custom_attendance_string)
                
            #     # worksheet.write(row, 4, record.custom_hours_worked_string)
            #     worksheet.write_merge(row, row, 4, 5, record.custom_hours_worked_string)
                
            #     # worksheet.write(row, 6, record.custom_hours_lost_string)
            #     worksheet.write_merge(row, row, 6, 7, record.custom_hours_lost_string)
                
            #     # worksheet.write(row, 8, "{:.2f}%".format(record.utilisation_percentage))
            #     worksheet.write_merge(row, row, 8, 9, "{:.2f}%".format(record.utilisation_percentage))
                
                serial_number += 1

            #     # worksheet.write(row, 0, employee_name)
            #     # worksheet.write(row, 1, record.custom_attendance_string)
            #     # worksheet.write(row, 2, record.custom_hours_worked_string)
            #     # worksheet.write(row, 3, record.custom_hours_lost_string)
            #     # worksheet.write(row, 5, record.overtime_hour)
            #     # worksheet.write(row, 4, "{:.2f}%".format(record.utilisation_percentage))
            #     # row += 1            
            
        # worksheet.write(row, 1, record.working_hours)
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


