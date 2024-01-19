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

            field_names = ['Sr.#', 'STUDENT NAME', 'FATHER NAME', '6 DIGIT ID', 'CLASS', 'SECTION', 'BRANCH', 'WITHDRAWN', 'ADM. DATE', 'SECURITY','ACTIVE/INACTIVE']

            for col, field_name in enumerate(field_names):
                worksheet.write_merge(0, 0, col*1, col*1, field_name, style=style_title)

            
            # account_move_object = self.env['account.move'].search([])
            # domain = [('move_type', '=', 'out_refund')]
            # searching with filter that move_type is of out_refund type which is of Reversal
            # account_move_object = self.env['account.move'].search(domain)
            count_students=0
            row = 1
            serial_number = 1
            enrolled_students = self.env['school.student'].search([])
            # raise UserError(enrolled_students)
            # done=[]
            # unique_student_ids = []
            # students = self.env['school.student'].search([])
            # for student in students:
            #     accounts = self.env['account.move'].search([
            #         ("move_type", "=", "out_refund"),
            #         ("x_student_id_cred", "=", student.id)
            #     ])

            #     for move in accounts:
            #         if move.x_student_id_cred.id not in unique_student_ids:
            #             unique_student_ids.append(move.x_student_id_cred.id)

            # unique_student_ids_tuple = tuple(unique_student_ids)


            # HAMZA NAVEED
            reversals = self.env['account.move'].search([("move_type","=","out_refund"),('journal_id.name','=','Security Deposit')])
            serial_number = 1
            
            if reversals:
                for reversal in reversals:

                    worksheet.write(row, 0, serial_number)

                    if reversal.x_student_id_cred.name:
                        worksheet.write(row, 1, reversal.x_student_id_cred.name)
                    else:
                        worksheet.write(row, 1, "N/A")

                    
                    if reversal.partner_id.name:
                        worksheet.write(row, 2, reversal.partner_id.name)
                    else:
                        worksheet.write(row, 2, "N/A")


                    if reversal.x_student_id_cred.facts_id:
                        worksheet.write(row, 3, reversal.x_student_id_cred.facts_udid)
                    else:
                        worksheet.write(row, 3, "N/A")


                    if reversal.x_student_id_cred.grade_level_ids:
                        for grade in reversal.x_student_id_cred.grade_level_ids:
                            worksheet.write(row, 4, grade.name)
                            break
                    elif reversal.class_name:
                        worksheet.write(row, 4, reversal.class_name)
                    else:
                        worksheet.write(row, 4, "N/A")

                    
                    if reversal.x_student_id_cred.homeroom:
                        worksheet.write(row, 5, reversal.x_student_id_cred.homeroom)
                    # elif reversal.student_ids:
                    #     student = self.env['school.student'].search([('id','=',reversal.student_ids.id)])
                    #     if student:
                    #         homeroom = student.homeroom
                    #         if homeroom != False:
                    #             vals = homeroom.split('-')
                    #             if vals[-1].isalpha():
                    #                 worksheet.write(row, 5, vals[-1])
                    #             else:
                    #                 student = self.env['school.student'].search([('id','=',reversal.student_ids.id)])
                    #                 if student:
                    #                     homeroom = student.homeroom
                    #                     if homeroom != False:
                    #                         vals = homeroom.split('-')
                    #                         if vals[-1].isalpha():
                    #                             worksheet.write(row, 5, vals[-1])
                    #                         else:
                    #                             worksheet.write(row, 5, "N/A")
                    else:
                        worksheet.write(row, 5, "N/A")


                    if reversal.x_student_id_cred.x_last_school_id :
                        worksheet.write(row, 6, reversal.x_student_id_cred.x_last_school_id.name)
                    elif reversal.std_current_branch:
                        worksheet.write(row, 6, reversal.std_current_branch)
                    else:
                        worksheet.write(row, 6, "N/A")


                    if reversal.withdrawn_status_reversal:
                        worksheet.write(row, 7, reversal.withdrawn_status_reversal)
                        
                    else:
                        worksheet.write(row, 7, "N/A")

                    
                    # if reversal.invoice_date:
                    #     worksheet.write(row, 8, str(reversal.invoice_date))
                    # else:
                    #     worksheet.write(row, 8, "N/A")
                    
                    if reversal.x_studio_admission_date_1:
                        worksheet.write(row, 8, str(reversal.x_studio_admission_date_1))
                    else:
                        worksheet.write(row, 8, "N/A")
                    # adm_flag = False

                    # bills = self.env['account.move'].search([('student_ids', '=', reversal.x_student_id_cred.id)])
                    # for bill in bills:
                    #     if bill.journal_id.name == "Admission Challan":
                    #         worksheet.write(row, 8, str(bill.x_studio_admission_date_1))
                    #         adm_flag = True
                    #         break
                    
                    # # not found admission date
                    # if adm_flag == False:
                    #     for history in reversal.x_student_id_cred.enrollment_history_ids:
                    #         if history.enrollment_status_id.name == "Admission":
                    #             worksheet.write(row, 8, history.timestamp.strftime("%Y-%m-%d"))
                    #             adm_flag = True
                    #             break
                    
                    # # still not found admission date
                    # if adm_flag == False:
                    #     worksheet.write(row, 8, "N/A")


                    flag = False
                    for line in reversal.invoice_line_ids:
                        if line.account_id.name == 'Security Fee' and line.price_total!=0:
                            worksheet.write(row, 9, line.price_total)
                            flag = True
                            break
                            
                    # Security Fee not found
                    if flag == False:
                        bills = self.env['account.move'].search([('student_ids', '=', reversal.x_student_id_cred.id)])
                        for bill in bills:
                            for line in bill.invoice_line_ids:
                                if line.account_id.name == 'Security Fee' and line.price_total!=0:
                                    worksheet.write(row, 9, line.price_total)
                                    flag = True
                                    break
                            if flag == True:
                                break    
                    
                    # Security Fee still not found
                    if flag == False:
                        worksheet.write(row, 9, "-")

    
                                
                                

                    
                    
                    if reversal.x_studio_enrolled_cred.name:
                        if reversal.x_studio_enrolled_cred.name == "Enrolled":
                            worksheet.write(row, 10, "Y")
                        else:
                            worksheet.write(row, 10, "N")
                    else:
                        worksheet.write(row, 10, "N/A")


                    serial_number += 1
                    row += 1

            # HAMZA NAVEED




            # for student in enrolled_students:
            #     admission = self.env['account.move'].search([("move_type","=","out_invoice"),('journal_id.name','=','Admission Challan'), ('state','=','posted'), ("student_ids","in",[student.id])], limit=1)
            #     reversal = self.env['account.move'].search([("move_type","=","out_refund"),('journal_id.name','=','Security Deposit'),("x_student_id_cred","=",student.id)], limit=1)


            #     # if admission:
            #     #     for line in admission.invoice_line_ids:
            #     #         if line.account_id.name == 'Security Fee':
            #     #             worksheet.write(row, 0, serial_number)
    
            #     #     # for adm in admission:
            #     #     #     for line in adm.invoice_line_ids:
            #     #     #         if line.account_id.name == 'Security Fee' and student not in done:
            #     #     #             worksheet.write(row, 0, serial_number)
    
            #     #             if student.name:
            #     #                 worksheet.write(row, 1, student.name)
            #     #             else:
            #     #                 worksheet.write(row, 1, "N/A")
    
            #     #             if admission.partner_id.name:
            #     #                 worksheet.write(row, 2, admission.partner_id.name)
            #     #             else:
            #     #                 worksheet.write(row, 2, "N/A")
    
            #     #             if student.facts_udid:
            #     #                 worksheet.write(row, 3, student.facts_udid)
            #     #             else:
            #     #                 worksheet.write(row, 3, "N/A")
                            
            #     #             if student.grade_level_ids:
            #     #                 worksheet.write(row, 4, student.grade_level_ids.name)
            #     #             elif admission.class_name:
            #     #                 worksheet.write(row, 4, admission.class_name)
            #     #             else:
            #     #                 worksheet.write(row, 4, "N/A")
            #     #             if student.homeroom:
            #     #                 worksheet.write(row, 5, student.homeroom)
            #     #             elif admission.student_ids:
            #     #                 student = self.env['school.student'].search([('id','=',admission.student_ids.id)])
            #     #                 if student:
            #     #                     homeroom = student.homeroom
            #     #                     if homeroom != False:
            #     #                         vals = homeroom.split('-')
            #     #                         if vals[-1].isalpha():
            #     #                             worksheet.write(row, 5, vals[-1])
            #     #                         else:
            #     #                             student = self.env['school.student'].search([('id','=',reversal.student_ids.id)])
            #     #                             if student:
            #     #                                 homeroom = student.homeroom
            #     #                                 if homeroom != False:
            #     #                                     vals = homeroom.split('-')
            #     #                                     if vals[-1].isalpha():
            #     #                                         worksheet.write(row, 5, vals[-1])
            #     #                                     else:
            #     #                                         worksheet.write(row, 5, "N/A")
            #     #             else:
            #     #                 worksheet.write(row, 5, "N/A")
    
            #     #             if student.id :
            #     #                 if student.x_last_school_id :
            #     #                     worksheet.write(row, 6, student.x_last_school_id.name)
            #     #             elif admission.std_current_branch:
            #     #                 worksheet.write(row, 6, admission.std_current_branch)
            #     #             else:
            #     #                 worksheet.write(row, 6, "N/A")
    
            #     #             if admission.withdrawn_status_bill:
            #     #                 worksheet.write(row, 7, admission.withdrawn_status_bill)
                                
            #     #             elif reversal.withdrawn_status_reversal:
            #     #                 worksheet.write(row, 7, reversal.withdrawn_status_reversal)
                                
            #     #             else:
            #     #                 # raise UserError(str('Admission ')+str(admission.id))
            #     #                 worksheet.write(row, 7, "N/A")
    
            #     #             if admission.invoice_date:
            #     #                 worksheet.write(row, 8, str(admission.invoice_date))
            #     #             else:
            #     #                 worksheet.write(row, 8, "N/A")
                             
            #     #             if line.account_id.name == 'Security Fee':
            #     #                 worksheet.write(row, 9, line.price_total)
            #     #             # elif line.account_id.name != 'Security Fee':
            #     #             #     for rev_line in reversal.invoice_line_ids:
            #     #             #         if rev_line.account_id.name == 'Security Fee':
            #     #             #             worksheet.write(row, 9, rev_line.price_total)
                                    
            #     #             else:
            #     #                 worksheet.write(row, 9, "N/A")
    
            #     #             # done.append(student)
            #     #             #adding active / inactive column
            #     #             if student.enrollment_status_ids:
            #     #                 for status in student.enrollment_status_ids:
            #     #                     if status.name == 'Enrolled':
            #     #                         worksheet.write(row, 10, 'Y')
            #     #                         break
            #     #                     else:
            #     #                         worksheet.write(row, 10, 'N')
            #     #             # else:
            #     #             #     worksheet.write(row, 10, "N/A")
                            
            #     #             serial_number += 1
            #     #             row+=1
                            
            #     # else:
            #     #     # pass
            #     if reversal:
            #         for line in reversal.invoice_line_ids:
            #             if line.account_id.name == 'Security Fee':
            #                 worksheet.write(row, 0, serial_number)
            #                 if student.name:
            #                     worksheet.write(row, 1, student.name)
            #                 else:
            #                     worksheet.write(row, 1, "N/A")
    
            #                 if reversal.partner_id.name:
            #                     worksheet.write(row, 2, reversal.partner_id.name)
            #                 else:
            #                     worksheet.write(row, 2, "N/A")
    
            #                 if student.facts_udid:
            #                     worksheet.write(row, 3, student.facts_udid)
            #                 else:
            #                     worksheet.write(row, 3, "N/A")
            #                 # for grade in student.grade_level_ids:

            #                 if student.grade_level_ids:
            #                     for grade in student.grade_level_ids:
            #                         worksheet.write(row, 4, grade.name)
            #                         break
            #                 # elif admission.class_name:
            #                 #     worksheet.write(row, 4, admission.class_name)
            #                 elif reversal.class_name:
            #                     worksheet.write(row, 4, reversal.class_name)
            #                 else:
            #                     worksheet.write(row, 4, "N/A")
            #                 if student.homeroom:
            #                     worksheet.write(row, 5, student.homeroom)
            #                 # elif admission.student_ids:
            #                 #     student = self.env['school.student'].search([('id','=',admission.student_ids.id)])
            #                 elif reversal.student_ids:
            #                     student = self.env['school.student'].search([('id','=',reversal.student_ids.id)])
            #                     if student:
            #                         homeroom = student.homeroom
            #                         if homeroom != False:
            #                             vals = homeroom.split('-')
            #                             if vals[-1].isalpha():
            #                                 worksheet.write(row, 5, vals[-1])
            #                             else:
            #                                 student = self.env['school.student'].search([('id','=',reversal.student_ids.id)])
            #                                 if student:
            #                                     homeroom = student.homeroom
            #                                     if homeroom != False:
            #                                         vals = homeroom.split('-')
            #                                         if vals[-1].isalpha():
            #                                             worksheet.write(row, 5, vals[-1])
            #                                         else:
            #                                             worksheet.write(row, 5, "N/A")
            #                 else:
            #                     worksheet.write(row, 5, "N/A")
    
            #                 if student.id :
            #                     if student.x_last_school_id :
            #                         worksheet.write(row, 6, student.x_last_school_id.name)
            #                 # elif admission.std_current_branch:
            #                 #     worksheet.write(row, 6, admission.std_current_branch)
            #                 elif reversal.std_current_branch:
            #                     worksheet.write(row, 6, reversal.std_current_branch)
            #                 else:
            #                     worksheet.write(row, 6, "N/A")
    
            #                 # if admission.withdrawn_status:
            #                 #     worksheet.write(row, 7, admission.withdrawn_status)
            #                 if reversal.withdrawn_status_reversal:
            #                     worksheet.write(row, 7, reversal.withdrawn_status_reversal)
                                
            #                 else:
            #                     # raise UserError(str('Reversal ')+str(reversal.id))
            #                     worksheet.write(row, 7, "N/A")
    
            #                 if reversal.invoice_date:
            #                     worksheet.write(row, 8, str(reversal.invoice_date))
            #                 else:
            #                     worksheet.write(row, 8, "N/A")
                                
            #                 if line.account_id.name == 'Security Fee':
            #                     worksheet.write(row, 9, line.price_total)
            #                 # elif line.account_id.name != 'Security Fee':
            #                 #     for rev_line in admission.invoice_line_ids:
            #                 #         if rev_line.account_id.name == 'Security Fee':
            #                 #             worksheet.write(row, 9, rev_line.price_total)
                                    
            #                 else:
            #                     worksheet.write(row, 9, "N/A")
            #                 if student.enrollment_status_ids:
            #                     enrolled = False
            #                     for status in student.enrollment_status_ids:
            #                         if status.name == 'Enrolled':
            #                             enrolled = True
            #                             break

            #                     if enrolled:
            #                         worksheet.write(row, 10, 'Y')
            #                     else:
            #                         worksheet.write(row, 10, 'N')
            #                 else:
            #                     worksheet.write(row, 10, "N/A")    
            #                 # if student.enrollment_status_ids:
            #                 #     for status in student.enrollment_status_ids:
            #                 #         if status.name == 'Enrolled':
            #                 #             worksheet.write(row, 10, 'Y')
            #                 #             break
            #                 #         else:
            #                 #             worksheet.write(row, 10, 'N')
            #                 # else:
            #                 #     worksheet.write(row, 10, "N/A")
            #                 count_students+=1
            #                 serial_number += 1
            #                 row+=1
            #                     # done.append(student)

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
