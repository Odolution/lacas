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



            # Step 1: Search for students in school.student using facts_id
            
            all_students = self.env['school.student'].search([])
            all_student_ids = [student.id for student in all_students]

            # raise UserError(student_ids)
            # Create a set to store the unique student ids
            unique_student_ids = set()

            # Step 2: Search for students in out_invoice (Admission Challan) with product_id==Security
            invoice_domain = [('move_type', '=', 'out_invoice'), ('journal_id', '=', 'Admission Challan'),('student_ids','in',all_student_ids)]
            all_invoice_objects = self.env['account.move'].search(invoice_domain)
            for line in all_invoice_objects.invoice_line_ids:
                if line.product_id.name == "Security":
                    for student in all_invoice_objects.student_ids:
                        unique_student_ids.add(student.id)

            raise UserError(list(unique_student_ids))
            
            

            # Step 3: Search for students in out_refund (Reversal) with product_id==Security
            refund_domain = [('move_type', '=', 'out_refund'),('student_ids','in',all_student_ids)]
            all_refund_objects = self.env['account.move'].search(refund_domain)

            # Add unique student ids to the set if product_id==Security
            for line in all_refund_objects.invoice_line_ids:
                if line.product_id.name == "Security":
                    unique_student_ids.add(all_refund_objects.student_ids)
            
            raise UserError(list(unique_student_ids))

            domain = [('student_ids', 'in', all_student_ids)]
            all_account_move_objects = self.env['account.move'].search(domain)

        
            # Step 4: Write the results in an Excel file
            row = 1
            serial_number = 1

            for student_object in all_account_move_objects:
                flag=False
                # raise UserError(student_object.student_ids[0].id) 
                for std_id in student_object.student_ids:
                    if std_id.id in list(unique_student_ids):
                        flag=True
                        break
                if flag == True:
                    # Student found in either out_invoice or out_refund with product_id==Security
                    worksheet.write(row, 0, serial_number)
                    worksheet.write(row, 1, student_object.name if student_object.name else "N/A")
                    worksheet.write(row, 2, student_object.partner_id.name if student_object.partner_id else "N/A")
                    worksheet.write(row, 3, student_object.udid_cred_custom if student_object.udid_cred_custom else "N/A")
                    worksheet.write(row, 4, student_object.class_name if student_object.class_name else "N/A")
                    worksheet.write(row, 5, student_object.section_name if student_object.section_name else "N/A")
                    worksheet.write(row, 6, student_object.x_school_id_cred.name if student_object.x_school_id_cred else "N/A")
                    worksheet.write(row, 7, student_object.x_studio_withdrawn_status if student_object.x_studio_withdrawn_status else "N/A")
                    worksheet.write(row, 8, str(student_object.x_studio_admission_date) if student_object.x_studio_admission_date else "N/A")
                    for line in student_object.invoice_line_ids:
                        if line.product_id.name=="Security":
                            worksheet.write(row, 9, line.price_total if line.price_total or line.price_total==0 else "N/A")
                    
                else:
                    # Student not found in out_invoice or out_refund with product_id==Security
                    worksheet.write(row, 0, serial_number)
                    worksheet.write(row, 1, student_object.name if student_object.name else "N/A")
                    worksheet.write(row, 2, student_object.partner_id.name if student_object.partner_id else "N/A")
                    worksheet.write(row, 3, student_object.udid_cred_custom if student_object.udid_cred_custom else "N/A")
                    worksheet.write(row, 4, student_object.class_name if student_object.class_name else "N/A")
                    worksheet.write(row, 5, student_object.section_name if student_object.section_name else "N/A")
                    worksheet.write(row, 6, student_object.x_school_id_cred.name if student_object.x_school_id_cred else "N/A")
                    worksheet.write(row, 7, student_object.x_studio_withdrawn_status if student_object.x_studio_withdrawn_status else "N/A")
                    worksheet.write(row, 8, str(student_object.x_studio_admission_date) if student_object.x_studio_admission_date else "N/A")
                    worksheet.write(row, 9, "N/A")

                # Add more fields as needed
                serial_number += 1
                row += 1
            #     else:
            #         # Student not found in out_invoice or out_refund with product_id==Security
            #         worksheet.write(row, 0, serial_number)
            #         worksheet.write(row, 1, student.name if student.name else "N/A")
            #         # worksheet.write(row, 2, student.partner_id.name if student.partner_id else "N/A")
            #         # worksheet.write(row, 3, student.udid_cred_custom if student.udid_cred_custom else "N/A")
            #         # worksheet.write(row, 4, student.class_name if student.class_name else "N/A")
            #         # worksheet.write(row, 5, student.section_name if student.section_name else "N/A")
            #         # worksheet.write(row, 6, student.x_school_id_cred.name if student.x_school_id_cred else "N/A")
            #         # worksheet.write(row, 7, student.x_studio_withdrawn_status if student.x_studio_withdrawn_status else "N/A")
            #         # worksheet.write(row, 8, str(student.x_studio_admission_date) if student.x_studio_admission_date else "N/A")
            #         # worksheet.write(row, 9, "N/A")
                    
                    
            #         # Add more fields as needed
            #         serial_number += 1
            #         row += 1



            # Define the search domain with "or" between move_type and "and" between move_type and journal_id
            # domain = ['|', ('move_type', '=', 'out_invoice'), ('move_type', '=', 'out_refund'), ('move_type', '=', 'out_invoice'), ('journal_id', '=', 'Admission Challan')]

            # # Search for records matching the combined domain
            # all_account_move_objects = self.env['account.move'].search(domain)

            # row = 1
            # serial_number = 1

            # # Process the records based on move_type and journal_id
            # for individual_object in all_account_move_objects:
            #     for line in individual_object.invoice_line_ids:
            #         if line.product_id.name == "Security":
            #             worksheet.write(row, 0, serial_number)
            #             worksheet.write(row, 1, individual_object.x_student_id_cred.name if individual_object.x_student_id_cred else "N/A")
            #             worksheet.write(row, 2, individual_object.partner_id.name if individual_object.partner_id else "N/A")
            #             worksheet.write(row, 3, individual_object.udid_cred_custom if individual_object.udid_cred_custom else "N/A")
            #             worksheet.write(row, 4, individual_object.class_name if individual_object.class_name else "N/A")
            #             worksheet.write(row, 5, individual_object.section_name if individual_object.section_name else "N/A")
            #             worksheet.write(row, 6, individual_object.x_school_id_cred.name if individual_object.x_school_id_cred else "N/A")
            #             worksheet.write(row, 7, individual_object.x_studio_withdrawn_status if individual_object.x_studio_withdrawn_status else "N/A")
            #             worksheet.write(row, 8, str(individual_object.x_studio_admission_date) if individual_object.x_studio_admission_date else "N/A")
            #             worksheet.write(row, 9, line.price_total if line.price_total or line.price_total==0 else "N/A")
            #             serial_number += 1
            #             row += 1
            #         else:
            #             pass


            # domain = [('move_type', '=', 'out_refund')]
            # # searching with filter that move_type is of out_refund type which is of Reversal
            # all_account_move_objects = self.env['account.move'].search(domain)
            # row = 1
            # serial_number = 1

            
            # for individual_object in all_account_move_objects:
            #     for line in individual_object.invoice_line_ids:
            #         if line.product_id.name == "Security":
            #             worksheet.write(row, 0, serial_number)

            #             if line.product_id.name == "Security":
            #                 # worksheet.write_merge(row, row, 1, 1, individual_object.x_student_id_cred.name)
            #                 worksheet.write(row, 1, individual_object.x_student_id_cred.name)
            #             else:
            #                 worksheet.write(row, 1, "N/A")

            #             if individual_object.partner_id.name:
            #                 worksheet.write(row, 2, individual_object.partner_id.name)
            #             else:
            #                 worksheet.write(row, 2, "N/A")

            #             if individual_object.udid_cred_custom:
            #                 worksheet.write(row, 3, individual_object.udid_cred_custom)
            #             else:
            #                 worksheet.write(row, 3, "N/A")
                        
            #             if individual_object.class_name:
            #                 worksheet.write(row, 4, individual_object.class_name)
            #             else:
            #                 worksheet.write(row, 4, "N/A")

            #             if individual_object.section_name:
            #                 worksheet.write(row, 5, individual_object.section_name)
            #             else:
            #                 worksheet.write(row, 5, "N/A")

            #             if individual_object.x_school_id_cred.name:
            #                 worksheet.write(row, 6, individual_object.x_school_id_cred.name)
            #             else:
            #                 worksheet.write(row, 6, "N/A")

            #             if individual_object.x_studio_withdrawn_status:
            #                 worksheet.write(row, 7, individual_object.x_studio_withdrawn_status)
            #             else:
            #                 worksheet.write(row, 7, "N/A")

            #             if individual_object.x_studio_admission_date:
            #                 worksheet.write(row, 8, str(individual_object.x_studio_admission_date))
            #             else:
            #                 worksheet.write(row, 8, "N/A")

            #             if line.price_total:
            #                 worksheet.write(row, 9, line.price_total)
            #             elif line.price_total==0:
            #                 worksheet.write(row, 9, 0)
            #             else:
            #                 worksheet.write(row, 9, "N/A")

            #             serial_number += 1
            #             row+=1
            #             # raise UserError(line.name)
            #         else:
            #             pass
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


