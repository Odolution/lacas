
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


class Student(models.Model):
    _inherit='account.move'

    current_enrollment_status_dev= fields.Many2one(related= 'student_ids_ol.x_last_enrollment_status_id',readonly=True,store=True,string='Enrollment status for devlopment')



class AccountMoveReport(models.TransientModel):
    _name = 'billing.student.report.line'
    
    record_id=fields.Char('ID')
    branch_name=fields.Char('name')
    total_Issuance_billing =fields.Float('total_Issuance_billing')
    with_out_Withdrawn_billing =fields.Float('with_out_Withdrawn_billing')
    total_Recovery_paid =fields.Float('total_Recovery_paid')
    total_bad_debt =fields.Float('total_bad_debt')
   
    

class RecoveryReportWizard(models.TransientModel):
    _name="billing.cycle.report.wizard"
    _description='billing cycle summary report Wizard'

    
    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    from_date_pay = fields.Date(string='From')
    to_date_pay = fields.Date(string='To')
    
    account_report_line=fields.Many2many('billing.student.report.line', string='Account report Line')
    # by_account_report_line=fields.Many2many('student.bi.monthly.report.line', string='Account by Monthly report Line')
    
    def _date_constrains(self):
        if not self.to_date or not self.from_date:
            raise UserError("Sorry, you must enter all dates..")
        
        
        if not self.from_date and not self.to_date :
            raise UserError("Sorry, you must enter dates..")
        
        else:

            from_year=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y')
            to_year=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%y')
            from_month=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%m')
            to_month=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%m')
            # raise UserError(from_year)

            if self.to_date < self.from_date:
                # raise UserError(datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y'))

                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

        if not self.to_date_pay or not self.from_date_pay:
            raise UserError("Sorry, you must enter all dates..")
        
        
        if not self.from_date_pay and not self.to_date_pay :
            raise UserError("Sorry, you must enter dates..")
        
        else:

            pay_from_year=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%y')
            pay_to_year=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%y')

            pay_from_month=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%m')
            pay_to_month=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%m')
            # raise UserError(from_year)

            if self.to_date_pay < self.from_date_pay:
                # raise UserError(datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y'))

                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))


    def action_print_report(self):
        lines=[]
        school_ids= []
        total_Issuance_billing_list={}
        with_out_Withdrawn_billing_list={}
        total_Recovery_paid_list={}
        total_bad_debts_list={}

        school_ids_raw=self.env['school.school'].search([])
        school_ids_raw = school_ids_raw.sorted(lambda o : o.name)

        pay_from_month=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%m')
        pay_from_year=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%y')

        pay_to_month=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%m')
        pay_to_year=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%y')

        for rec in school_ids_raw:
            if rec.name !="Milestone Model Town (Matric)":
            #     continue
                school_ids.append(rec)
            # raise UserError(rec) Milestone Model Town (Matric) or Milestone Model Town Senior Campus
           
            school_bill_ids = self.env['account.move'].search([
                ('x_studio_previous_branch', '=', rec.name),
                ('move_type','=','out_invoice'),
                ('state', '=', 'posted'),
               ('invoice_date',">=",self.from_date),('invoice_date',"<=",self.to_date)
            ])

            if rec.name in ("Milestone Model Town (Matric)"):
                select_new="Milestone Model Town Senior Campus"
            else:
                select_new=rec.name

            total_count=0
            with_out_Withdrawn=0
            total_Recovery_paid=0
            total_bad_debt=0
            for bill_rec in school_bill_ids:           
                # total_count += float(bill_rec.amount_total)
                total_count += float(bill_rec.net_amount)
                if bill_rec.student_ids.x_last_enrollment_status_id.name !="Withdrawn":
                    # with_out_Withdrawn += float(bill_rec.amount_total)
                    with_out_Withdrawn += float(bill_rec.net_amount)
                elif bill_rec.student_ids.x_last_enrollment_status_id.name =="Withdrawn" and bill_rec.payment_state =="not_paid":
                    total_bad_debt += float(bill_rec.net_amount)
                
                if bill_rec.payment_state =="paid":
                    if bill_rec.ol_payment_date:
                        payment_date = bill_rec.ol_payment_date
                        month_in_payment = payment_date.strftime('%m')
                        year_in_payment = payment_date.strftime('%y')

                        if pay_from_year <= year_in_payment <= pay_to_year and pay_from_month <= month_in_payment <= pay_to_month:
                            # total_Recovery_paid += float(bill_rec.amount_total)
                            total_Recovery_paid += float(bill_rec.net_amount)


            total_Issuance_billing_list[select_new] = total_count
            with_out_Withdrawn_billing_list[select_new] = with_out_Withdrawn
            total_Recovery_paid_list[select_new] = total_Recovery_paid
            total_bad_debts_list[select_new] = total_bad_debt
    



        for item in range(len(school_ids)):
            name_view = school_ids[item].name
            billing_view = total_Issuance_billing_list[name_view]
            with_out_Withdrawn_billing = with_out_Withdrawn_billing_list[name_view]
            total_Recovery_paid_final = total_Recovery_paid_list[name_view]
            total_bad_debts_final = total_bad_debts_list[name_view]
            mvl=self.env['billing.student.report.line'].create({
                                        
                "branch_name":name_view,
                "total_Issuance_billing":billing_view,
                "with_out_Withdrawn_billing":with_out_Withdrawn_billing,
                "total_Recovery_paid":total_Recovery_paid_final,
                "total_bad_debt":total_bad_debts_final,
            })
            lines.append(mvl.id)
        
        self.write({
            "account_report_line":[(6,0,lines)]
        })  


    def action_print_excel_billing_report(self):
        
        self._date_constrains()

        self.action_print_report()

        if xlwt:
            global billing_counts ,by_monthly_billing_counts,select_by_monthly_list
            
            filename = 'Percentage wise billing cycle summary report v2.xls'
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            
            style_title = xlwt.easyxf(
            " align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            # header = xlwt.easyxf('pattern: pattern solid;'
            # "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            header = xlwt.easyxf('font: bold on, color black;'
                           'pattern: pattern solid, fore_colour gray25;'
                           'align: vertical center, horiz center;'
                           'border: top thin, bottom thin, right thin, left thin') 
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
            formatted_date_from = self.from_date.strftime('%b-%Y')
            formatted_date_to = self.to_date.strftime('%d-%b-%Y')
            date_string= 'Billing '+str(formatted_date_from)+ str(' %')+"age wise recovery As on "+ str(formatted_date_to)
            worksheet.write_merge(0,0,2,7,date_string, style=header)

            worksheet.write_merge(3,4,0,0, 'S#',  style=red_style_title)
            worksheet.write_merge(3,4,1,1, 'Branch',  style=red_style_title)
            worksheet.write_merge(3,4,2,2, 'Total Issuance',  style=red_style_title)
            worksheet.write_merge(3,4,3,3, 'Net Billing Exc.Withdrawals',  style=red_style_title)
            worksheet.write_merge(3,4,4,4, 'Total Recovery',  style=red_style_title)
            worksheet.write_merge(3,4,5,5, 'Receivables',  style=red_style_title)
            worksheet.write_merge(3,4,6,6, 'Total',  style=red_style_title)
            worksheet.write_merge(3,4,7,7, 'Bad Debts',  style=red_style_title)
            worksheet.write_merge(3,4,8,8, "'%'age of Recovery on '\n' Enrolled and Paid Bills",  style=red_style_title)
            worksheet.write_merge(3,4,9,9, "Actual Recovery '%'age",  style=red_style_title)
            worksheet.write_merge(3,4,10,10, "Count of enrolled students with Un-Paid status",  style=red_style_title)
            # worksheet.(0,1,0,3,"",)

            total_total_Issuance_billing=0
            total_with_out_Withdrawn_billing=0
            total_total_Recovery_paid=0
            total_Receivables=0
            total_Total=0
            total_Bade_Dabts=0
            total_total_Issuance_billing_branch=0
            total_with_out_Withdrawn_billing_branch=0
            total_total_Recovery_paid_branch=0
            total_Receivables_branch=0
            total_Total_branch=0
            total_Bade_Dabts_branch=0
            total_enrolled_unpaid_student_count=0
            total_enrolled_unpaid_student_count_branch=0
            row=5
            col=4
            count = 0
            first_record =self.account_report_line[0] 
            first_record= first_record.branch_name.lower()
            b_split= first_record.split(' ')
            match= b_split[0]+' '+b_split[1]
            for rec in self.account_report_line:
                if rec:       
                    b= rec.branch_name.lower()  
                    bills = self.env['account.move'].search(
                        [
                            ('x_studio_previous_branch', '=', rec.branch_name),
                            ('move_type', '=', 'out_invoice'),
                            ('state', '=', 'posted'),
                            ('current_enrollment_status_dev.name', '=', 'Enrolled'),
                            ('payment_state', '=', 'not_paid'),
                            ('invoice_date', '>=', self.from_date),
                            ('invoice_date', '<=', self.to_date),
                        ])
                    enrolled_unpaid_student_count = len(set(bills.mapped('student_ids_ol.id')))
                    if b.startswith(match) and (b != 'lacas johar town boys' ) and (b != 'milestone model town senior campus' ):
                        total_total_Issuance_billing_branch += rec.total_Issuance_billing
                        total_with_out_Withdrawn_billing_branch += rec.with_out_Withdrawn_billing
                        total_total_Recovery_paid_branch += rec.total_Recovery_paid
                        Receivables = rec.total_Issuance_billing - rec.total_Recovery_paid
                        Total = Receivables + rec.total_Recovery_paid
                        Bade_Dabts = rec.total_Issuance_billing - Total
                        total_Receivables_branch += Receivables
                        total_Total_branch += Total
                        total_Bade_Dabts_branch += rec.total_bad_debt
                        total_enrolled_unpaid_student_count_branch+= enrolled_unpaid_student_count
                    else:
                        b_split= b.split(' ')
                        match= b_split[0]+' '+b_split[1]
                        worksheet.write_merge(row,row,0,0, '',  style=red_style_title)
                        worksheet.write_merge(row,row,1,1, 'Total',  style=red_style_title)
                        worksheet.write_merge(row,row,2,2, total_total_Issuance_billing_branch,  style=red_style_title)
                        worksheet.write_merge(row,row,3,3,total_with_out_Withdrawn_billing_branch ,  style=red_style_title)
                        worksheet.write_merge(row,row,4,4,total_total_Recovery_paid_branch,  style=red_style_title)
                        worksheet.write_merge(row,row,5,5,total_Receivables_branch,  style=red_style_title)
                        worksheet.write_merge(row,row,6,6,total_Total_branch,  style=red_style_title)
                        # worksheet.write_merge(row,row,7,7,total_Bade_Dabts_branch,  style=red_style_title)
                        worksheet.write_merge(row,row,7,7,total_Bade_Dabts_branch,  style=red_style_title)
                        if total_total_Recovery_paid_branch and total_with_out_Withdrawn_billing_branch:
                            total_Recovery_on_Enrolled_and_Paid_Bills_branch = (total_total_Recovery_paid_branch/total_with_out_Withdrawn_billing_branch)*100
                        else:
                            total_Recovery_on_Enrolled_and_Paid_Bills_branch = 0
                        worksheet.write_merge(row,row,8,8,  str(f"{total_Recovery_on_Enrolled_and_Paid_Bills_branch:.1f}")+"%" ,  style=red_style_title)
                        if total_total_Recovery_paid_branch and total_total_Issuance_billing_branch:
                            Total_Actual_Recovery_branch = (total_total_Recovery_paid_branch/total_total_Issuance_billing_branch)*100
                        else:
                            Total_Actual_Recovery_branch = 0
                        worksheet.write_merge(row,row,9,9, str(f"{Total_Actual_Recovery_branch:.1f}")+"%",  style=red_style_title)
                        worksheet.write_merge(row,row,10,10,total_enrolled_unpaid_student_count_branch ,  style=red_style_title)
                        row+=1

                        total_total_Issuance_billing_branch = rec.total_Issuance_billing
                        total_with_out_Withdrawn_billing_branch = rec.with_out_Withdrawn_billing
                        total_total_Recovery_paid_branch = rec.total_Recovery_paid
                        Receivables = rec.total_Issuance_billing - rec.total_Recovery_paid
                        Total = Receivables + rec.total_Recovery_paid
                        Bade_Dabts = rec.total_Issuance_billing - Total
                        total_Receivables_branch = Receivables
                        total_Total_branch = Total                        
                        total_Bade_Dabts_branch = rec.total_bad_debt
                        total_enrolled_unpaid_student_count_branch= enrolled_unpaid_student_count

                    
                    count +=1
                    worksheet.write_merge(row,row,0,0,count, style=style_title)
                    worksheet.write_merge(row,row,1,1,rec.branch_name, style=style_title)
                    worksheet.write_merge(row,row,2,2,rec.total_Issuance_billing, style=style_title)
                    worksheet.write_merge(row,row,3,3,rec.with_out_Withdrawn_billing, style=style_title)
                    worksheet.write_merge(row,row,4,4,rec.total_Recovery_paid, style=style_title)
                    Receivables = rec.total_Issuance_billing - rec.total_Recovery_paid
                    worksheet.write_merge(row,row,5,5,Receivables, style=style_title)
                    Total = Receivables + rec.total_Recovery_paid
                    worksheet.write_merge(row,row,6,6,Total, style=style_title)
                    Bade_Dabts = rec.total_Issuance_billing - Total
                    # worksheet.write_merge(row,row,7,7,Bade_Dabts, style=style_title)
                    worksheet.write_merge(row,row,7,7,rec.total_bad_debt, style=style_title)
                    if rec.total_Recovery_paid and rec.with_out_Withdrawn_billing:
                        Recovery_on_Enrolled_and_Paid_Bills = (rec.total_Recovery_paid/rec.with_out_Withdrawn_billing)*100
                    else:
                        Recovery_on_Enrolled_and_Paid_Bills = 0
                    worksheet.write_merge(row,row,8,8,str(f"{Recovery_on_Enrolled_and_Paid_Bills:.1f}")+"%", style=style_title)
                    if rec.total_Recovery_paid and rec.total_Issuance_billing:
                        Actual_Recovery = (rec.total_Recovery_paid/rec.total_Issuance_billing)*100
                    else:
                        Actual_Recovery = 0
                    worksheet.write_merge(row,row,9,9,str(f"{Actual_Recovery:.1f}")+"%", style=style_title)
                    worksheet.write_merge(row,row,10,10,enrolled_unpaid_student_count, style=style_title)

                    total_total_Issuance_billing += rec.total_Issuance_billing
                    total_with_out_Withdrawn_billing += rec.with_out_Withdrawn_billing
                    total_total_Recovery_paid += rec.total_Recovery_paid
                    total_Receivables += Receivables
                    total_Total += Total
                    total_Bade_Dabts += rec.total_bad_debt
                    total_enrolled_unpaid_student_count+= enrolled_unpaid_student_count

                    row+=1
            
            worksheet.write_merge(row,row,0,0, '',  style=red_style_title)
            worksheet.write_merge(row,row,1,1, 'Total',  style=red_style_title)
            worksheet.write_merge(row,row,2,2, total_total_Issuance_billing,  style=red_style_title)
            worksheet.write_merge(row,row,3,3,total_with_out_Withdrawn_billing ,  style=red_style_title)
            worksheet.write_merge(row,row,4,4,total_total_Recovery_paid,  style=red_style_title)
            worksheet.write_merge(row,row,5,5,total_Receivables,  style=red_style_title)
            worksheet.write_merge(row,row,6,6,total_Total,  style=red_style_title)
            # worksheet.write_merge(row,row,7,7,total_Bade_Dabts,  style=red_style_title)
            worksheet.write_merge(row,row,7,7,total_Bade_Dabts,  style=red_style_title)
            if total_total_Recovery_paid and total_with_out_Withdrawn_billing:
                total_Recovery_on_Enrolled_and_Paid_Bills = (total_total_Recovery_paid/total_with_out_Withdrawn_billing)*100
            else:
                total_Recovery_on_Enrolled_and_Paid_Bills = 0
            worksheet.write_merge(row,row,8,8,  str(f"{total_Recovery_on_Enrolled_and_Paid_Bills:.1f}")+"%" ,  style=red_style_title)
            if total_total_Recovery_paid and total_total_Issuance_billing:
                Total_Actual_Recovery = (total_total_Recovery_paid/total_total_Issuance_billing)*100
            else:
                Total_Actual_Recovery = 0
            worksheet.write_merge(row,row,9,9, str(f"{Total_Actual_Recovery:.1f}")+"%",  style=red_style_title)
            worksheet.write_merge(row,row,10,10,total_enrolled_unpaid_student_count ,  style=red_style_title)

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
        