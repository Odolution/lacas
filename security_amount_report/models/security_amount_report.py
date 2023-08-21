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

            domain = [('move_type', '=', 'out_refund')]
            # searching with filter that move_type is of out_refund type which is of Reversal
            all_account_move_objects = self.env['account.move'].search(domain)
            row = 1
            serial_number = 1

            
            for individual_object in all_account_move_objects:
                for line in individual_object.invoice_line_ids:
                    if line.product_id.name == "Security":
                        worksheet.write(row, 0, serial_number)

                        if line.product_id.name == "Security":
                            # worksheet.write_merge(row, row, 1, 1, individual_object.x_student_id_cred.name)
                            worksheet.write(row, 1, individual_object.x_student_id_cred.name)
                        else:
                            worksheet.write(row, 1, "N/A")

                        if individual_object.partner_id.name:
                            worksheet.write(row, 2, individual_object.partner_id.name)
                        else:
                            worksheet.write(row, 2, "N/A")

                        if individual_object.udid_cred_custom:
                            worksheet.write(row, 3, individual_object.udid_cred_custom)
                        else:
                            worksheet.write(row, 3, "N/A")
                        
                        if individual_object.class_name:
                            worksheet.write(row, 4, individual_object.class_name)
                        else:
                            worksheet.write(row, 4, "N/A")

                        if individual_object.section_name:
                            worksheet.write(row, 5, individual_object.section_name)
                        else:
                            worksheet.write(row, 5, "N/A")

                        if individual_object.x_school_id_cred.name:
                            worksheet.write(row, 6, individual_object.x_school_id_cred.name)
                        else:
                            worksheet.write(row, 6, "N/A")

                        if individual_object.x_studio_withdrawn_status:
                            worksheet.write(row, 7, individual_object.x_studio_withdrawn_status)
                        else:
                            worksheet.write(row, 7, "N/A")

                        if individual_object.x_studio_admission_date:
                            worksheet.write(row, 8, str(individual_object.x_studio_admission_date))
                        else:
                            worksheet.write(row, 8, "N/A")

                        if individual_object.security_amnt_lv:
                            worksheet.write(row, 9, individual_object.security_amnt_lv)
                        else:
                            worksheet.write(row, 9, "N/A")

                        serial_number += 1
                        row+=1
                        # raise UserError(line.name)
                    else:
                        pass
                        # raise UserError("No Security Found")
                        # raise UserError(str(account_move_object))

            # row = 11
            # serial_number = 1
            # for record in account_move_object.student_ids:
                # worksheet.write_merge(row, row, 0, 1, serial_number)
                # worksheet.write_merge(row, row, 0, 1, record.x_student_id_cred.name)
                # worksheet.write_merge(row, row, 0, 1, account_move_object.partner_id.name)
                # worksheet.write_merge(row, row, 0, 1, account_move_object.udid_cred_custom)
                # worksheet.write_merge(row, row, 0, 1, serial_number)
                # worksheet.write_merge(row, row, 0, 1, serial_number)
                # worksheet.write_merge(row, row, 0, 1, serial_number)
                # worksheet.write_merge(row, row, 0, 1, serial_number)
                # worksheet.write_merge(row, row, 0, 1, serial_number)
                # worksheet.write_merge(row, row, 0, 1, serial_number)
                # worksheet.write_merge(row, row, 0, 1, serial_number)
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
                
                # serial_number += 1

            #     # worksheet.write(row, 0, employee_name)
            #     # worksheet.write(row, 1, record.custom_attendance_string)
            #     # worksheet.write(row, 2, record.custom_hours_worked_string)
            #     # worksheet.write(row, 3, record.custom_hours_lost_string)
            #     # worksheet.write(row, 5, record.overtime_hour)
            #     # worksheet.write(row, 4, "{:.2f}%".format(record.utilisation_percentage))
                # row += 1            
            
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

