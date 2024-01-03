
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


def format_with_commas(number):
    return "{:,}".format(int(number))



class AccountMoveReport(models.TransientModel):
    _name = 'student.report.line'
    
    record_id=fields.Char('ID')
    branch_name=fields.Char('name')
    school_bill_len =fields.Float('Total')
    billing_list_paid =fields.Float('Paid')

class ByMonthlyAccountMoveReport(models.TransientModel):
    _name = 'student.bi.monthly.report.line'
    
    record_id=fields.Char('ID')
    branch_name=fields.Char('name')
    school_bill_len =fields.Float('Total')
    billing_list_paid =fields.Float('Paid')
    

class RecoveryReportWizard(models.TransientModel):
    _name="school.branch.report.wizard"
    _description='Print school Branch Wizard'

    
    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    from_date_pay = fields.Date(string='From')
    to_date_pay = fields.Date(string='To')
    
    account_report_line=fields.Many2many('student.report.line', string='Account report Line')
    by_account_report_line=fields.Many2many('student.bi.monthly.report.line', string='Account by Monthly report Line')
    

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

            if from_year and to_year :

                if  from_year < '22' or from_year >'23':
                    raise UserError("Sorry, Year must be between 2022-2023..")
                    raise ValidationError(_('Sorry, Year must be 2022-2023...'))

                elif to_year <"22" or to_year >"23":
                    raise UserError("Sorry, Year must be between 2022-2023..")
                    raise ValidationError(_('Sorry, Year must be 2022-2023...'))
        
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

            if from_year and to_year :

                if  pay_from_year < from_year or pay_to_year > to_year:
                    raise UserError("Sorry, Invalid year range..")
                    raise ValidationError(_('Sorry, Invalid year range...'))

                elif pay_from_month < from_month:
                    raise UserError("Sorry, Invalid month range..")
                    raise ValidationError(_('Sorry, Invalid month range...'))


    def list_months(self):
        next_month = self.to_date + relativedelta(months=1)
        first_day_of_next_month = next_month.replace(day=1)

        # Subtract one day from the first day of the next month to get the last day of the current month
        last_day_of_month = first_day_of_next_month - relativedelta(days=1)


        # Initialize the result list
        covered_months = []

        # Iterate over each month within the duration
        current_month = self.from_date
        while current_month <= last_day_of_month:
            # Format the month as "Mon-YY" (e.g., Feb-22)
            month_str = current_month.strftime("%b-%y")

            # Add the formatted month to the result list
            covered_months.append(month_str)

            # Move to the next month
            current_month += relativedelta(months=1)
        
        return covered_months

    def by_monthly_calculation(self):
        global month_dict 
        selected_month = self.list_months()
        month_dict = {"January": 1,"Jan": 1,"February": 2,"Feb": 2,"March": 3,"Mar": 3,"April": 4,"Apr": 4,"May": 5,"June": 6,"Jun": 6,"July": 7,"Jul": 7,"August": 8,"Aug": 8,"September": 9,"Sep": 9,"October": 10,"Oct": 10,"November": 11,"Nov": 11,"December": 12,"Dec": 12}
        
        by_sort_by_monthly_list = self.env['account.move'].search([
            # ('x_studio_previous_branch', '=', rec.name),
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice'),
            ('journal_id', '=', 126),
            
        ])

        combinations = []
        final_combinations = []

        # Separate the list into sublists for each year
        yearly_lists = {}
        for item in selected_month:
            month, year = item.split("-")
            if year not in yearly_lists:
                yearly_lists[year] = []
            yearly_lists[year].append(month)

        # Create combinations of all two-month pairs within the same year
        for year, months in yearly_lists.items():
            for i in range(len(months) - 1):
                for j in range(i + 1, len(months)):
                    combination = f"{months[i]}-{months[j]}-{year}"
                    combinations.append(combination)

        for item in combinations:
            month_start1 , month_end1, and_year1 = item.split('-')
            condition1 = str(month_dict.get(month_start1.capitalize()))+"-"+str(month_dict.get(month_end1.capitalize()))+"-"+and_year1

            for invoice in by_sort_by_monthly_list:
                # raise UserError(invoice.bill_date)
                if not invoice.bill_date:
                    continue
                
                # Split the bill_date into parts and check the format
                date_parts = invoice.bill_date.split('-')
                if len(date_parts) == 3:
                    month_start , month_end, and_year = invoice.bill_date.split('-')
                    condition2 = str(month_dict.get(month_start.capitalize())) +"-"+str(month_dict.get(month_end.capitalize()))+"-"+and_year 
                    # raise UserError(str(condition1)+"==="+str(condition1))
                    if condition1 == condition2:
                        if invoice.bill_date not in final_combinations:
                            final_combinations.append(item)
        
        # Create a new list to store unique items
        unique_final_combinations_list = []

        for item in final_combinations:
            if item not in unique_final_combinations_list:
                unique_final_combinations_list.append(item)
        return unique_final_combinations_list
        # raise UserError(unique_final_combinations_list)

    def action_print_report(self):

        lines=[]
        by_lines=[]
        school_ids = []
        billing_list={}
        billing_list_paid={}
        by_monthly_billing_list={}
        by_monthly_billing_list_paid={}
        global billing_counts , billing_counts_paid , by_monthly_billing_counts, by_monthly_billing_counts_paid ,select_by_monthly_list,month_dict
        billing_counts = {}
        billing_counts_paid = {} # HAMZA NAVEED
        by_monthly_billing_counts = {}
        by_monthly_billing_counts_paid = {} # HAMZA NAVEED


        select_by_monthly_list=self.by_monthly_calculation()
        # raise UserError(select_by_monthly_list)

        school_ids_raw=self.env['school.school'].search([])
        school_ids_raw = school_ids_raw.sorted(lambda o : o.name)

        v_from_month=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%m')
        v_from_year=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y')

        v_to_month=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%m')
        v_to_year=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%y')

        # Convert year and month pairs to a comparable format (like integers or date objects)
        v_start_period = v_from_year * 12 + v_from_month
        v_end_period = v_to_year * 12 + v_to_month
        # Adjust for year-end rollover
        if v_end_period < v_start_period:
            v_end_period += 12


        pay_from_month=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%m')
        pay_from_year=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%y')

        pay_to_month=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%m')
        pay_to_year=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%y')


        # Convert year and month pairs to a comparable format (like integers or date objects)
        start_period = pay_from_year * 12 + pay_from_month
        end_period = pay_to_year * 12 + pay_to_month

        # Adjust for year-end rollover
        if end_period < start_period:
            end_period += 12

        for rec in school_ids_raw:
            if rec.name !="Milestone Model Town (Matric)":
            #     continue
                school_ids.append(rec)
            # raise UserError(rec) Milestone Model Town (Matric) or Milestone Model Town Senior Campus
           
            school_bill_ids = self.env['account.move'].search([
                ('x_studio_previous_branch', '=', rec.name),
                ('state', '=', 'posted'),
                ('move_type','=','out_invoice'),('journal_id','=',125)
            ])

            if rec.name in ("Milestone Model Town (Matric)"):
                select_new="Milestone Model Town Senior Campus"
            else:
                select_new=rec.name

            total_count=0
            total_count_paid=0
            for bill_rec in school_bill_ids:
                invoice_date = bill_rec.invoice_date
                month_in_invoice = invoice_date.strftime('%m')
                year_in_invoice = invoice_date.strftime('%y')
                
                v_payment_period = year_in_invoice * 12 + month_in_invoice

                # Check if the invoice date is within the specified range
                if v_from_year <= year_in_invoice <= v_to_year and v_start_period <= v_payment_period <= v_end_period:
                    # Create a key using the month and year
                    month_key = f"{select_new}-{year_in_invoice}-{month_in_invoice}"

                    
                    if bill_rec.payment_state =="paid":
                        if bill_rec.ol_payment_date:
                            payment_date = bill_rec.ol_payment_date
                            month_in_payment = payment_date.strftime('%m')
                            year_in_payment = payment_date.strftime('%y')
                            payment_period = year_in_payment * 12 + month_in_payment
                            
                            if pay_from_year <= year_in_payment <= pay_to_year and start_period <= payment_period <= end_period:
                                total_count_paid += float(bill_rec.net_amount)
                                # HAMZA NAVEED
                                if month_key in billing_counts_paid:
                                    billing_counts_paid[month_key] += float(bill_rec.net_amount)
                                else:
                                    billing_counts_paid[month_key] = float(bill_rec.net_amount)



                    if month_key in billing_counts:
                        billing_counts[month_key] += float(bill_rec.net_amount)
                        total_count += float(bill_rec.net_amount)
                    else:
                        billing_counts[month_key] = float(bill_rec.net_amount)
                        total_count += float(bill_rec.net_amount)

            billing_list_paid[select_new] = total_count_paid
            billing_list[select_new] = total_count
    
            for year in range(int(v_from_year), int(v_to_year) + 1):
                for month in range(int(v_from_month), int(v_to_month) + 1):
                    month_key = f"{select_new}-{str(year)[-2:]}-{month:02}"
                    if month_key not in billing_counts:
                        billing_counts[month_key] = 0
                    # HAMZA NAVEED
                    if month_key not in billing_counts_paid:
                        billing_counts_paid[month_key] = 0
           
            # raise UserError(billing_counts)


        # message = "PAID Billing Counts:\n\n"
        # for month_key, count in billing_counts_paid.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"
            
        # message += "\n\n\n\n"
        # message += "PAID Billing Information:\n\n"
        # for month_key, count in billing_list_paid.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"

        # message += "\n\n\n\n"
        # message += "Billing Counts:\n\n"
        # for month_key, count in billing_counts.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"
            
        # message += "\n\n\n\n"
        # message += "Billing Information:\n\n"
        # for month_key, count in billing_list.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"
            
        # # Raise a UserError with the summarized message
        # raise UserError(message)
        

        for item in range(len(school_ids)):
            name_view = school_ids[item].name
            billing_view = billing_list[name_view]
            billing_paid_view = billing_list_paid[name_view]
            mvl=self.env['student.report.line'].create({
                                        
                "branch_name":name_view,
                "school_bill_len":billing_view,
                "billing_list_paid":billing_paid_view,
            })
            lines.append(mvl.id)


        self.write({
            "account_report_line":[(6,0,lines)]
        })  
        # raise UserError(school_ids.name)

# Bi Monthly==========================================

        for rec in school_ids_raw:
            by_school_bill_ids = self.env['account.move'].search([
                ('x_studio_previous_branch', '=', rec.name),
                ('state', '=', 'posted'),
                ('move_type','=','out_invoice'),('journal_id','=',126)
            ])
            # raise UserError(str(rec.name)+" "+str(by_school_bill_ids))
            if rec.name in ("Milestone Model Town (Matric)"):
                select_new="Milestone Model Town Senior Campus"
            else:
                select_new=rec.name

            total_count=0
            total_count_paid=0
            for month_in_list in select_by_monthly_list:
                month_start1 , month_end1, and_year1 = month_in_list.split('-')
                condition1 = str(month_dict.get(month_start1.capitalize()))+"-"+str(month_dict.get(month_end1.capitalize()))+"-"+and_year1
                
                month_key = f"{select_new}-{month_in_list}"
                
                for bill_rec in by_school_bill_ids:
                    if not bill_rec.bill_date:
                        continue
               
                    date_parts = bill_rec.bill_date.split('-')
                    if len(date_parts) == 3:
                        month_start , month_end, and_year = date_parts
                        condition2 = str(month_dict.get(month_start.capitalize())) +"-"+str(month_dict.get(month_end.capitalize()))+"-"+and_year 
                    
                        if condition1==condition2:
                            if bill_rec.payment_state =="paid":
                                if bill_rec.ol_payment_date:
                                    payment_date = bill_rec.ol_payment_date
                                    month_in_payment = payment_date.strftime('%m')
                                    year_in_payment = payment_date.strftime('%y')

                                    if pay_from_year <= year_in_payment <= pay_to_year and pay_from_month <= month_in_payment <= pay_to_month:
                                        formatted_net_amount='{:,}'.format(bill_rec.net_amount)
                
                                        #total_count_paid += float(bill_rec.net_amount)
                                        total_count_paid += formatted_net_amount
                                        
                                        # HAMZA NAVEED
                                        if month_key in by_monthly_billing_counts_paid:
                                            by_monthly_billing_counts_paid[month_key] += float(bill_rec.net_amount)
                                        else:
                                            by_monthly_billing_counts_paid[month_key] = float(bill_rec.net_amount)



                            if month_key in by_monthly_billing_counts:
                                by_monthly_billing_counts[month_key] += float(bill_rec.net_amount)
                                total_count += float(bill_rec.amount_total)
                            else:
                                by_monthly_billing_counts[month_key] = float(bill_rec.net_amount)
                                total_count += float(bill_rec.amount_total)
                if month_key not in by_monthly_billing_counts:
                    by_monthly_billing_counts[month_key]=0
                # HAMZA NAVEED
                if month_key not in by_monthly_billing_counts_paid:
                    by_monthly_billing_counts_paid[month_key]=0

                by_monthly_billing_list_paid[select_new] = total_count_paid
                by_monthly_billing_list[select_new] = total_count
        
        # raise UserError(" "+str(by_monthly_billing_list))

        if select_by_monthly_list:
            for item in range(len(school_ids)):

                name_view = school_ids[item].name


                
                billing_view = by_monthly_billing_list[name_view]
                billing_paid_view = by_monthly_billing_list_paid[name_view]

                mvl2=self.env['student.bi.monthly.report.line'].create({
                    "branch_name":name_view,
                    "school_bill_len":billing_view,
                    "billing_list_paid":billing_paid_view,
                })
                by_lines.append(mvl2.id)


            self.write({
                "by_account_report_line":[(6,0,by_lines)]
            })  

        # message = "PAID Billing Counts:\n\n"
        # for month_key, count in by_monthly_billing_counts_paid.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"
            
        # message += "\n\n\n\n"
        # message += "PAID Billing Information:\n\n"
        # for month_key, count in by_monthly_billing_list_paid.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"

        # message += "\n\n\n\n"
        # message += "Billing Counts:\n\n"
        # for month_key, count in by_monthly_billing_counts.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"
            
        # message += "\n\n\n\n"
        # message += "Billing Information:\n\n"
        # for month_key, count in by_monthly_billing_list.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"
            
        # # Raise a UserError with the summarized message
        # raise UserError(message)


    def action_print_excel_school_branch_report(self):
        
        

        self.action_print_report()
        
        
        if xlwt:
            global billing_counts, billing_counts_paid ,by_monthly_billing_counts, by_monthly_billing_counts_paid, select_by_monthly_list
            
            filename = 'Students Branch Report.xls'
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('Students Branch Std')
            

            header = xlwt.easyxf('font: bold on, color black;'
                           'pattern: pattern solid, fore_colour gray25;'
                           'align: vertical center, horiz center;'
                           'border: top thin, bottom thin, right thin, left thin') 
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
            
            formatted_date_from = self.from_date.strftime('%b-%Y')
            formatted_date_to = self.to_date.strftime('%d-%b-%Y')
            date_string= 'Billing  '+str(formatted_date_from)+" cycle wise average '%' of recovery As on "+ str(formatted_date_to)
            worksheet.write_merge(0,0,2,7,date_string, style=header)


            v_from_month=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%m')
            v_from_year=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y')

            v_to_month=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%m')
            v_to_year=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%y')
            # raise UserError(str(v_from_month)+" "+str(v_from_year)+" "+str(v_to_month)+" "+str(v_to_year))
            months= {
                1:['01','JAN-22',10,'22'],
                2:['02','FEB-22',20,'22'],
                3:['03','MAR-22',30,'22'],
                4:['04','APR-22',40,'22'],
                5:['05','MAY-22',50,'22'],
                6:['06','JUN-22',60,'22'],
                7:['07','JUL-22',70,'22'],
                8:['08','AUG-22',80,'22'],
                9:['09','SEP-22',90,'22'],
                10:['10','OCT-22',100,'22'],
                11:['11','NOV-22',110,'22'],
                12:['12','DEC-22',120,'22'],
                13:['01','JAN-23',130,'23'],
                14:['02','FEB-23',140,'23'],
                15:['03','MAR-23',150,'23'],
                16:['04','APR-23',160,'23'],
                17:['05','MAY-23',170,'23'],
                18:['06','JUN-23',180,'23'],
                19:['07','JUL-23',190,'23'],
                20:['08','AUG-23',200,'23'],
                21:['09','SEP-23',200,'23'],
                22:['10','OCT-23',200,'23'],
                23:['11','NOV-23',200,'23'],
                24:['12','DEC-23',200,'23'],
                25:['01','JAN-24',130,'24'],
                26:['02','FEB-24',140,'24'],
                27:['03','MAR-24',150,'24'],
                28:['04','APR-24',160,'24'],
                29:['05','MAY-24',170,'24'],
                30:['06','JUN-24',180,'24'],
                31:['07','JUL-24',190,'24'],
                32:['08','AUG-24',200,'24'],
                33:['09','SEP-24',200,'24'],
                34:['10','OCT-24',200,'24'],
                35:['11','NOV-24',200,'24'],
                36:['12','DEC-24',200,'24'],
                }
            range_start = 0
            range_stop = 0
            # raise UserError(v_to)
            for key, value in months.items():
                if value[0] == v_from_month and value[3] == v_from_year:
                    range_start = key
                if value[0] == v_to_month and value[3] == v_to_year:

                    range_stop = key

            worksheet.write_merge(2,3,0,0,"Current Branch/School", style=red_style_title)
            # worksheet.write_merge(0,1,4,5,"Billing month Jul-23",style=red_style_title)
            
            
            col = 1
            
            # raise UserError(str(range_start)+" "+str(range_stop))
      
            for i in range(range_start,range_stop+1):
                # raise UserError(months[i][0]+" "+months[i][3])
                worksheet.write_merge(2,3,col,col,'Issuance '+months[i][1],red_style_title)
                col+=1
                worksheet.write_merge(2,3,col,col,'RECOVERY '+months[i][1],red_style_title)
                # worksheet.write_merge(row,row,col,col+1,months[i][2])
                col+=1
            # # if select_by_monthly_list:
            #     worksheet.write_merge(0,1,col,col+1,"Total",style=red_style_title)
            #     worksheet.write_merge(0,1,col+2,col+4,"Branch Wise Recovery",style=red_style_title)
            #     worksheet.write_merge(0,1,col+5,col+6,"'%' age of Recovery",style=yellow_style_title)
            #     worksheet.write_merge(2,3,col,col+1,"Total", lime_style_title)   
            
                # print('col:',months[i][1], 'data:',months[i][2])
            group_total=0
            final_total=0
            group_recovery=0
            final_recovery=0
            group_name_list=[]
            months_total_dict={}
            months_recovery_dict={} # HAMZA NAVEED
            months_row_total_dict={}
            months_row_paid_dict={}
            row=4
            col=1
            for rec in self.account_report_line:
                if rec:
                #    Total
                    new_string = rec.branch_name
                    new_substring = new_string.split(' ')[0] + ' ' + new_string.split(' ')[1]

                    if len(group_name_list)==0:
                        group_name_list.append(rec.branch_name)
                        group_total+=rec.school_bill_len
                        group_recovery+=rec.billing_list_paid

                        for i in range(range_start,range_stop+1):
                            row_month_total=0
                            new_month_key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                            for month_key, count in billing_counts.items():
                                if new_month_key==month_key:
                                    key = f"{new_substring}-{months[i][3]}-{months[i][0]}"
                                    row_month_total= months_total_dict.get(key, 0)+count
                                    months_total_dict.update({key: row_month_total})
                            
                            # HAMZA NAVEED
                            for month_key, count in billing_counts_paid.items():
                                if new_month_key==month_key:
                                    key = f"{new_substring}-{months[i][3]}-{months[i][0]}"
                                    row_month_total= months_recovery_dict.get(key, 0)+count
                                    months_recovery_dict.update({key: row_month_total})
                    else:
                        main_string = group_name_list[0]
                        substring = main_string.split(' ')[0] + ' ' + main_string.split(' ')[1]
                        # raise UserError(str(group_name_list)+"==="+str(group_total))
                        
                        if substring == new_substring:
                            group_name_list.append(rec.branch_name)
                            group_total+=rec.school_bill_len
                            # final_total+=rec.school_bill_len
                            group_recovery+=rec.billing_list_paid
                            for i in range(range_start,range_stop+1):
                                row_month_total=0
                                new_month_key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                                for month_key, count in billing_counts.items():
                                    if new_month_key==month_key:
                                        key = f"{new_substring}-{months[i][3]}-{months[i][0]}"
                                        row_month_total= months_total_dict.get(key, 0)+count
                                        months_total_dict.update({key: row_month_total})
                                # HAMZA NAVEED
                                for month_key, count in billing_counts_paid.items():
                                    if new_month_key==month_key:
                                        key = f"{new_substring}-{months[i][3]}-{months[i][0]}"
                                        row_month_total= months_recovery_dict.get(key, 0)+count
                                        months_recovery_dict.update({key: row_month_total})

                        else:
                            
                            col=1
                            # for month_key, count in months_total_dict.items():
                            #     original_string = month_key
                            #     split_parts = original_string.split('-')
                            #     result = split_parts[0]
                            #     if substring == result:
                            #         worksheet.write_merge(row,row,col,col+2,count, style=yellow_style_title)
                            #         col+=3
                                
                            # # HAMZA NAVEED
                            # for month_key, count in months_recovery_dict.items():
                            #     original_string = month_key
                            #     split_parts = original_string.split('-')
                            #     result = split_parts[0]
                            #     if substring == result:
                            #         worksheet.write_merge(row,row,col,col+2,count, style=yellow_style_title)
                            #         col+=3

                            # HAMZA NAVEED
                            for month_key in months_total_dict:
                                result = month_key.split('-')[0]
                                if substring == result:
                                    worksheet.write_merge(row,row,col,col,format_with_commas(int(months_total_dict[month_key])), style=yellow_style_title)
                                    col += 1
                                    if month_key in months_recovery_dict:
                                        value = int(months_recovery_dict[month_key])
                                        worksheet.write_merge(row, row, col, col, format_with_commas(value), style=yellow_style_title)
                                    else:
                                        # Handle the missing key, e.g., write a default value or log a warning
                                        worksheet.write_merge(row, row, col, col, 0, style=yellow_style_title)  # example with a default value

                                    # worksheet.write_merge(row,row,col,col,int(months_recovery_dict[month_key]), style=yellow_style_title)
                                    col += 1

                                    
                            worksheet.write_merge(row,row,0,0,"Total", style=yellow_style_title)

                            if not select_by_monthly_list:
                                worksheet.write_merge(row,row,col,col,format_with_commas(group_total), style=yellow_style_title)
                                worksheet.write_merge(row,row,col+1,col+1,format_with_commas(group_recovery), style=yellow_style_title)
                                if group_recovery>0 and group_recovery>0:
                                    total_per_new =(group_recovery/group_total)*100
                                    worksheet.write_merge(row,row,col+2,col+2,str(round(total_per_new, 4))+' %',style=yellow_style_title)
                                else:
                                    worksheet.write_merge(row,row,col+2,col+2,'0 %',style=yellow_style_title)
                                # raise UserError(str(group_name_list)+"==="+str(group_total)+" =="+str(row))

                            row+=1
                            final_total+=group_total
                            final_recovery+=group_recovery
                            group_name_list.clear()
                            group_total=0
                            group_recovery=0

                            if rec.branch_name in ("LACAS Johar Town A Level","Milestone Model Town Campus","LACAS Gulberg Boys"):
                                # Print row data
                                worksheet.write_merge(row,row,0,0,rec.branch_name, style=style_title)
                                col=1
                                for i in range(range_start,range_stop+1):
                                    # check=True
                                    new_month_key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                                    for month_key, count in billing_counts.items():
                                        if new_month_key==month_key:
                                            worksheet.write_merge(row,row,col,col,format_with_commas(count),style=style_title)
                                    col+=1
                                # HAMZA NAVEED
                                for i in range(range_start,range_stop+1):
                                    # check=True
                                    new_month_key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                                    for month_key, count in billing_counts_paid.items():
                                        if new_month_key==month_key:
                                            worksheet.write_merge(row,row,col,col,format_with_commas(count),style=style_title)
                                    col+=1
                                
                                # add 
                                if select_by_monthly_list:
                                    months_row_total_dict.update({rec.branch_name:rec.school_bill_len })
                                    months_row_paid_dict.update({rec.branch_name:rec.billing_list_paid })
                                else:
                                    worksheet.write_merge(row,row,col,col,format_with_commas(rec.school_bill_len),style=style_title)
                                    worksheet.write_merge(row,row,col+1,col+1,format_with_commas(rec.billing_list_paid),style=style_title)
                                    if rec.school_bill_len>0 and rec.billing_list_paid>0:
                                        total_per =(rec.billing_list_paid/rec.school_bill_len)*100
                                        worksheet.write_merge(row,row,col+2,col+2,str(round(total_per, 4))+' %',style=style_title)
                                    else:
                                        worksheet.write_merge(row,row,col+2,col+2,'0 %',style=style_title)
                                row+=1

                                group_name_list.append(rec.branch_name)
                                group_total+=rec.school_bill_len
                                # final_total+=rec.school_bill_len
                                group_recovery+=rec.billing_list_paid
                                for i in range(range_start,range_stop+1):
                                    row_month_total=0
                                    new_month_key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                                    for month_key, count in billing_counts.items():
                                        if new_month_key==month_key:
                                            key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                                            row_month_total= months_total_dict.get(key, 0)+count
                                            months_total_dict.update({key: row_month_total})
                                    # HAMZA NAVEED
                                    for month_key, count in billing_counts_paid.items():
                                        if new_month_key==month_key:
                                            key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                                            row_month_total= months_recovery_dict.get(key, 0)+count
                                            months_recovery_dict.update({key: row_month_total})
                                col=1
                                # for month_key, count in months_total_dict.items():
                                #     original_string = month_key
                                #     split_parts = original_string.split('-')
                                #     result = split_parts[0]
                                #     if rec.branch_name == result:
                                #         worksheet.write_merge(row,row,col,col+2,count, style=yellow_style_title)
                                #         col+=3

                                # # HAMZA NAVEED
                                # for month_key, count in months_recovery_dict.items():
                                #     original_string = month_key
                                #     split_parts = original_string.split('-')
                                #     result = split_parts[0]
                                #     if rec.branch_name == result:
                                #         worksheet.write_merge(row,row,col,col+2,count, style=yellow_style_title)
                                #         col+=3

                                # HAMZA NAVEED
                                for month_key in months_total_dict:
                                    result = month_key.split('-')[0]
                                    if rec.branch_name == result:
                                        worksheet.write_merge(row,row,col,col,format_with_commas(int(months_total_dict[month_key])), style=yellow_style_title)
                                        col += 1
                                        if month_key in months_recovery_dict:
                                            value = int(months_recovery_dict[month_key])
                                            worksheet.write_merge(row, row, col, col, format_with_commas(value), style=yellow_style_title)
                                        else:
                                            # Handle the missing key, e.g., write a default value or log a warning
                                            worksheet.write_merge(row, row, col, col, 0, style=yellow_style_title)  # example with a default value

                                        # worksheet.write_merge(row,row,col,col,int(months_recovery_dict[month_key]), style=yellow_style_title)
                                        col += 1
                                        
                                worksheet.write_merge(row,row,0,0,"Total", style=yellow_style_title)

                                if not select_by_monthly_list:
                                    worksheet.write_merge(row,row,col,col,format_with_commas(group_total), style=yellow_style_title)
                                    worksheet.write_merge(row,row,col+1,col+1,format_with_commas(group_recovery), style=yellow_style_title)
                                    if group_recovery>0 and group_recovery>0:
                                        total_per_new =(group_recovery/group_total)*100
                                        worksheet.write_merge(row,row,col+2,col+2,str(round(total_per_new, 4))+' %',style=yellow_style_title)
                                    else:
                                        worksheet.write_merge(row,row,col+2,col+2,'0 %',style=yellow_style_title)
                                    # raise UserError(str(group_name_list)+"==="+str(group_total)+" =="+str(row))

                                row+=1
                                final_total+=group_total
                                final_recovery+=group_recovery
                                group_name_list.clear()
                                group_total=0
                                group_recovery=0

                                
                                continue
                                # raise UserError("LACAS Johar Town A Level")
                            else:

                                group_name_list.append(rec.branch_name)
                                group_total+=rec.school_bill_len
                                group_recovery+=rec.billing_list_paid
                                for i in range(range_start,range_stop+1):
                                    row_month_total=0
                                    new_month_key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                                    for month_key, count in billing_counts.items():
                                        if new_month_key==month_key:
                                            key = f"{new_substring}-{months[i][3]}-{months[i][0]}"
                                            row_month_total= months_total_dict.get(key, 0)+count
                                            months_total_dict.update({key: row_month_total})
                                    # HAMZA NAVEED
                                    for month_key, count in billing_counts_paid.items():
                                        if new_month_key==month_key:
                                            key = f"{new_substring}-{months[i][3]}-{months[i][0]}"
                                            row_month_total= months_recovery_dict.get(key, 0)+count
                                            months_recovery_dict.update({key: row_month_total})
                    
                    # Print row data
                    worksheet.write_merge(row,row,0,0,rec.branch_name, style=style_title)
                    col=1
                    for i in range(range_start,range_stop+1):
                        # check=True
                        new_month_key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                        for month_key, count in billing_counts.items():
                            if new_month_key==month_key:
                                worksheet.write_merge(row,row,col,col,format_with_commas(count),style=style_title)
                        col+=1
                        # HAMZA NAVEED
                        for month_key, count in billing_counts_paid.items():
                            if new_month_key==month_key:
                                worksheet.write_merge(row,row,col,col,format_with_commas(count),style=style_title)
                             
                        col+=1
                    
                    # add 
                    if select_by_monthly_list:
                        months_row_total_dict.update({rec.branch_name:rec.school_bill_len })
                        months_row_paid_dict.update({rec.branch_name:rec.billing_list_paid })
                    else:
                        worksheet.write_merge(row,row,col,col,format_with_commas(rec.school_bill_len),style=style_title)
                        worksheet.write_merge(row,row,col+1,col+1,format_with_commas(rec.billing_list_paid),style=style_title)
                        if rec.school_bill_len>0 and rec.billing_list_paid>0:
                            total_per =(rec.billing_list_paid/rec.school_bill_len)*100
                            worksheet.write_merge(row,row,col+2,col+2,str(round(total_per, 4))+' %',style=style_title)
                        else:
                            worksheet.write_merge(row,row,col+2,col+2,'0 %',style=style_title)
                    row+=1
         
        #  final total row
            worksheet.write_merge(row,row,0,0,"Total", style=yellow_style_title)

            col=1
            for i in range(range_start,range_stop+1):
                # check=True
                total=0
                test_year_month = f"{months[i][3]}-{months[i][0]}"
                for month_key, count in months_total_dict.items():
                    input_string = month_key
                    parts = input_string.split("-")
                    result = f"{parts[1]}-{parts[2]}"
                    # raise UserError(str(month_key)+" "+str(new_month_key))
                    if test_year_month==result:
                        total+=count

                worksheet.write_merge(row,row,col,col+2,total,style=yellow_style_title)
                col+=3

            # HAMZA NAVEED
            for i in range(range_start,range_stop+1):
                # check=True
                total=0
                test_year_month = f"{months[i][3]}-{months[i][0]}"
                for month_key, count in months_recovery_dict.items():
                    input_string = month_key
                    parts = input_string.split("-")
                    result = f"{parts[1]}-{parts[2]}"
                    # raise UserError(str(month_key)+" "+str(new_month_key))
                    if test_year_month==result:
                        total+=count

                worksheet.write_merge(row,row,col,col+2,total,style=yellow_style_title)
                col+=3

            # HAMZA NAVEED
            # for i in range(range_start,range_stop+1):
            #     # check=True
            #     total=0
            #     total_recovery = 0
            #     test_year_month = f"{months[i][3]}-{months[i][0]}"
                
            #     for month_key in months_total_dict:
            #         input_string = month_key
            #         parts = input_string.split("-")
            #         result = f"{parts[1]}-{parts[2]}"
            #         # raise UserError(str(month_key)+" "+str(new_month_key))
            #         if test_year_month==result:
            #             total+=months_total_dict[month_key]
            #             total_recovery += months_recovery_dict.get(month_key, 0)
            #     worksheet.write_merge(row,row,col,col,format_with_commas(total),style=yellow_style_title)
            #     col+=1
            #     worksheet.write_merge(row,row,col,col,format_with_commas(total_recovery),style=yellow_style_title)
            #     col+=1
            
            if not select_by_monthly_list:
                worksheet.write_merge(row,row,col,col,format_with_commas(final_total), style=yellow_style_title)
                worksheet.write_merge(row,row,col+1,col+1,format_with_commas(final_recovery), style=yellow_style_title)
                if final_total>0 and final_recovery>0:
                    final_total_per =(final_recovery/final_total)*100
                    worksheet.write_merge(row,row,col+2,col+2,str(round(final_total_per, 4))+' %',style=yellow_style_title)
           
#  # ++++++++++++++++++++++++BY monthy ++++++++++++++++++++++++++++++++++++++++

#             # message = "Billing information:\n\n"
#             # for month_key, count in months_row_paid_dict.items():
#             #     # month_key format: 'yy-mm'
#             #     # worksheet.write_merge(row,row,13,14,count,style=style_title)
#             #     message += f"Month: {month_key}, Number of bills: {count}\n"
                
#             # # Raise a UserError with the summarized message
#             # raise UserError(message)
            new_col=col
            # raise UserError(new_col)
            for month_in_list in select_by_monthly_list:
                # raise UserError(months[i][0]+" "+months[i][3])
                worksheet.write_merge(2,3,new_col,new_col,'Bi Monthly '+month_in_list,red_style_title)
                # worksheet.write_merge(row,row,new_col,new_col+1,months[i][2])
                new_col+=1
                # HAMZA NAVEED
                worksheet.write_merge(2,3,new_col,new_col,'Bi Monthly '+month_in_list+' RECOVERY',red_style_title)
                new_col+=1
            
            worksheet.write_merge(2,3,new_col,new_col,"Total",style=red_style_title)
            worksheet.write_merge(2,3,new_col+1,new_col+1,"Branch Wise Recovery",style=red_style_title)
            worksheet.write_merge(2,3,new_col+2,new_col+2,"'%' age of Recovery",style=yellow_style_title)

            group_total=0
            final_total=0
            group_recovery=0
            final_recovery=0
            new_group_name_list=[]
            new_months_total_dict={}
            new_months_recovery_dict={} # HAMZA NAVEED

            new_row=4
            new_col=col

            for rec in self.by_account_report_line:
                if rec:
                #    Total
                    new_string = rec.branch_name
                    new_substring = new_string.split(' ')[0] + ' ' + new_string.split(' ')[1]

                    if len(new_group_name_list)==0:
                        new_group_name_list.append(rec.branch_name)
                        group_total+=(rec.school_bill_len+months_row_total_dict.get(rec.branch_name))
                        group_recovery+=(rec.billing_list_paid+months_row_paid_dict.get(rec.branch_name))

                        for month_in_list in select_by_monthly_list:
                            row_month_total=0
                            new_month_key = f"{rec.branch_name}-{month_in_list}"
                            for month_key, count in by_monthly_billing_counts.items():
                                if new_month_key==month_key:
                                    key = f"{new_substring}-{month_in_list}"
                                    row_month_total= new_months_total_dict.get(key, 0)+count
                                    new_months_total_dict.update({key: row_month_total})
                            # HAMZA NAVEED
                            for month_key, count in by_monthly_billing_counts_paid.items():
                                if new_month_key==month_key:
                                    key = f"{new_substring}-{month_in_list}"
                                    row_month_total= new_months_recovery_dict.get(key, 0)+count
                                    new_months_recovery_dict.update({key: row_month_total})
                    else:
                        main_string = new_group_name_list[0]
                        substring = main_string.split(' ')[0] + ' ' + main_string.split(' ')[1]
                        # raise UserError(str(new_group_name_list)+"==="+str(group_total))
                        
                        if substring == new_substring:
                            new_group_name_list.append(rec.branch_name)
                            group_total+=(rec.school_bill_len+months_row_total_dict.get(rec.branch_name))
                            # final_total+=rec.school_bill_len
                            group_recovery+=(rec.billing_list_paid+months_row_paid_dict.get(rec.branch_name))
                            for month_in_list in select_by_monthly_list:
                                row_month_total=0
                                new_month_key = f"{rec.branch_name}-{month_in_list}"
                                for month_key, count in by_monthly_billing_counts.items():
                                    if new_month_key==month_key:
                                        key = f"{new_substring}-{month_in_list}"
                                        row_month_total= new_months_total_dict.get(key, 0)+count
                                        new_months_total_dict.update({key: row_month_total})
                                # HAMZA NAVEED
                                for month_key, count in by_monthly_billing_counts_paid.items():
                                    if new_month_key==month_key:
                                        key = f"{new_substring}-{month_in_list}"
                                        row_month_total= new_months_recovery_dict.get(key, 0)+count
                                        new_months_recovery_dict.update({key: row_month_total})

                        else:
                            
                            new_col=col
                            # for month_key, count in new_months_total_dict.items():
                            #     original_string = month_key
                            #     split_parts = original_string.split('-')
                            #     result = split_parts[0]
                            #     if substring == result:
                            #         result
                            #         worksheet.write_merge(new_row,new_row,new_col,new_col+2,count, style=yellow_style_title)
                            #         new_col+=3
                            # # HAMZA NAVEED
                            # for month_key, count in new_months_recovery_dict.items():
                            #     original_string = month_key
                            #     split_parts = original_string.split('-')
                            #     result = split_parts[0]
                            #     if substring == result:
                            #         #result
                            #         worksheet.write_merge(new_row,new_row,new_col,new_col+2,count, style=yellow_style_title)
                            #         new_col+=3
                            for month_key in new_months_total_dict:
                                result = month_key.split('-')[0]
                                if substring == result:
                                    worksheet.write_merge(new_row,new_row,new_col,new_col,new_months_total_dict[month_key], style=yellow_style_title)
                                    new_col += 1
                                    worksheet.write_merge(new_row,new_row,new_col,new_col,new_months_recovery_dict[month_key], style=yellow_style_title)
                                    new_col += 1


                                    
                            # worksheet.write_merge(new_row,new_row,0,3,"Total", style=yellow_style_title)
                            worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(group_total), style=yellow_style_title)
                            worksheet.write_merge(new_row,new_row,new_col+1,new_col+1,format_with_commas(group_recovery), style=yellow_style_title)
                            if group_recovery>0 and group_recovery>0:
                                total_per_new =(group_recovery/group_total)*100
                                worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,str(round(total_per_new, 4))+' %',style=yellow_style_title)
                            else:
                                worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,'0 %',style=yellow_style_title)
                            #  raise UserError(str(new_group_name_list)+"==="+str(group_total)+" =="+str(new_row))
                            new_row+=1
                            final_total+=group_total
                            final_recovery+=group_recovery
                            new_group_name_list.clear()
                            group_total=0
                            group_recovery=0

                            if rec.branch_name in ("LACAS Johar Town A Level","Milestone Model Town Campus","LACAS Gulberg Boys"):
                                # Print new_row data
                                # worksheet.write_merge(new_row,new_row,0,3,rec.branch_name, style=style_title)
                                new_col=col
                                for month_in_list in select_by_monthly_list:
                                    # check=True
                                    new_month_key = f"{rec.branch_name}-{month_in_list}"
                                    for month_key, count in by_monthly_billing_counts.items():
                                        if new_month_key==month_key:
                                            worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(count),style=style_title)
                                    new_col+=1
                                    # HAMZA NAVEED
                                    for month_key, count in by_monthly_billing_counts_paid.items():
                                        if new_month_key==month_key:
                                            worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(count),style=style_title)
                                        
                                    new_col+=1

                                both_total=rec.school_bill_len+months_row_total_dict.get(rec.branch_name)
                                both_total_paid=rec.billing_list_paid+months_row_paid_dict.get(rec.branch_name)
                                worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(both_total),style=style_title)
                                worksheet.write_merge(new_row,new_row,new_col+1,new_col+1,format_with_commas(both_total_paid),style=style_title)
                                if both_total>0 and both_total_paid>0:
                                    total_per =(both_total_paid/both_total)*100
                                    worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,str(round(total_per, 4))+' %',style=style_title)
                                else:
                                    worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,'0 %',style=style_title)
                                new_row+=1

                                new_group_name_list.append(rec.branch_name)
                                group_total+=both_total
                                # final_total+=rec.school_bill_len
                                group_recovery+=both_total_paid
                                for month_in_list in select_by_monthly_list:
                                    row_month_total=0
                                    new_month_key = f"{rec.branch_name}-{month_in_list}"
                                    for month_key, count in by_monthly_billing_counts.items():
                                        if new_month_key==month_key:
                                            key = f"{rec.branch_name}-{month_in_list}"
                                            row_month_total= new_months_total_dict.get(key, 0)+count
                                            new_months_total_dict.update({key: row_month_total})
                                    # HAMZA NAVEED
                                    for month_key, count in by_monthly_billing_counts_paid.items():
                                        if new_month_key==month_key:
                                            key = f"{rec.branch_name}-{month_in_list}"
                                            row_month_total= new_months_recovery_dict.get(key, 0)+count
                                            new_months_recovery_dict.update({key: row_month_total})
                                new_col=col
                                # for month_key, count in new_months_total_dict.items():
                                #     original_string = month_key
                                #     split_parts = original_string.split('-')
                                #     result = split_parts[0]
                                #     if rec.branch_name == result:
                                #         worksheet.write_merge(new_row,new_row,new_col,new_col+2,count, style=yellow_style_title)
                                #         new_col+=3
                                # # HAMZA NAVEED
                                # for month_key, count in new_months_recovery_dict.items():
                                #     original_string = month_key
                                #     split_parts = original_string.split('-')
                                #     result = split_parts[0]
                                #     if rec.branch_name == result:
                                #         worksheet.write_merge(new_row,new_row,new_col,new_col+2,count, style=yellow_style_title)
                                #         new_col+=3

                                # HAMZA NAVEED
                                for month_key in new_months_total_dict:
                                    original_string = month_key
                                    split_parts = original_string.split('-')
                                    result = split_parts[0]
                                    if rec.branch_name == result:
                                        worksheet.write_merge(new_row,new_row,new_col,new_col,new_months_total_dict[month_key], style=yellow_style_title)
                                        new_col+=1
                                        worksheet.write_merge(new_row,new_row,new_col,new_col,new_months_recovery_dict[month_key], style=yellow_style_title)
                                        new_col+=1


                                # worksheet.write_merge(new_row,new_row,0,3,"Total", style=yellow_style_title)
                                worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(group_total), style=yellow_style_title)
                                worksheet.write_merge(new_row,new_row,new_col+1,new_col+1,format_with_commas(group_recovery), style=yellow_style_title)
                                if group_recovery>0 and group_recovery>0:
                                    total_per_new =(group_recovery/group_total)*100
                                    worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,str(round(total_per_new, 4))+' %',style=yellow_style_title)
                                else:
                                    worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,'0 %',style=yellow_style_title)
                                #  raise UserError(str(new_group_name_list)+"==="+str(group_total)+" =="+str(new_row))
                                new_row+=1
                                final_total+=group_total
                                final_recovery+=group_recovery
                                new_group_name_list.clear()
                                group_total=0
                                group_recovery=0

                                
                                continue
                                # raise UserError("LACAS Johar Town A Level")
                            else:

                                new_group_name_list.append(rec.branch_name)
                                group_total+=(rec.school_bill_len+months_row_total_dict.get(rec.branch_name))
                                group_recovery+=(rec.billing_list_paid+months_row_paid_dict.get(rec.branch_name))
                                for month_in_list in select_by_monthly_list:
                                    row_month_total=0
                                    new_month_key = f"{rec.branch_name}-{month_in_list}"
                                    for month_key, count in by_monthly_billing_counts.items():
                                        if new_month_key==month_key:
                                            key = f"{new_substring}-{month_in_list}"
                                            row_month_total= new_months_total_dict.get(key, 0)+count
                                            new_months_total_dict.update({key: row_month_total})
                                    # HAMZA NAVEED
                                    for month_key, count in by_monthly_billing_counts_paid.items():
                                        if new_month_key==month_key:
                                            key = f"{new_substring}-{month_in_list}"
                                            row_month_total= new_months_recovery_dict.get(key, 0)+count
                                            new_months_recovery_dict.update({key: row_month_total})
                    
                    # Print row data
                    # worksheet.write_merge(row,row,0,3,rec.branch_name, style=style_title)
                    new_col=col

                    for month_in_list in select_by_monthly_list:
                        # check=True
                        new_month_key = f"{rec.branch_name}-{month_in_list}"
                        for month_key, count in by_monthly_billing_counts.items():
                            if new_month_key==month_key:
                                worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(count),style=style_title)
                        new_col+=1
                        # HAMZA NAVEED
                        for month_key, count in by_monthly_billing_counts_paid.items():
                            if new_month_key==month_key:
                                worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(count),style=style_title)
                        new_col+=1
                            
                    # new_row+=1
                    both_total=rec.school_bill_len+months_row_total_dict.get(rec.branch_name)
                    both_total_paid=rec.billing_list_paid+months_row_paid_dict.get(rec.branch_name)
                    worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(both_total),style=style_title)
                    worksheet.write_merge(new_row,new_row,new_col+1,new_col+1,format_with_commas(both_total_paid),style=style_title)
                    if both_total>0 and both_total_paid>0:
                        total_per =(both_total_paid/both_total)*100
                        worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,str(round(total_per, 4))+' %',style=style_title)
                    else:
                        worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,'0 %',style=style_title)
                    new_row+=1

            # final total row
            # worksheet.write_merge(row,row,0,3,"Total", style=yellow_style_title)

            new_col=col
            # for month_in_list in select_by_monthly_list:
            #     # check=True
            #     total=0
            #     test_year_month = f"{month_in_list}"
            #     for month_key, count in new_months_total_dict.items():
            #         input_string = month_key
            #         parts = input_string.split("-")
            #         result = f"{parts[1]}-{parts[2]}-{parts[3]}"
            #         # raise UserError(str(month_key)+" "+str(test_year_month))
            #         if test_year_month==result:
            #             total+=count

            #     worksheet.write_merge(new_row,new_row,new_col,new_col+2,total,style=yellow_style_title)
            #     new_col+=3

            # # HAMZA NAVEED
            # for month_in_list in select_by_monthly_list:
            #     # check=True
            #     total=0
            #     test_year_month = f"{month_in_list}"
            #     for month_key, count in new_months_recovery_dict.items():
            #         input_string = month_key
            #         parts = input_string.split("-")
            #         result = f"{parts[1]}-{parts[2]}-{parts[3]}"
            #         # raise UserError(str(month_key)+" "+str(test_year_month))
            #         if test_year_month==result:
            #             total+=count

            #     worksheet.write_merge(new_row,new_row,new_col,new_col+2,total,style=yellow_style_title)
            #     new_col+=3

            # HAMZA NAVEED
            for month_in_list in select_by_monthly_list:
                # check=True
                total=0
                total_recovery = 0
                test_year_month = f"{month_in_list}"
                for month_key in new_months_total_dict:
                    input_string = month_key
                    parts = input_string.split("-")
                    result = f"{parts[1]}-{parts[2]}-{parts[3]}"
                    # raise UserError(str(month_key)+" "+str(test_year_month))
                    if test_year_month==result:
                        total+=new_months_total_dict[month_key]
                        total_recovery+=new_months_recovery_dict[month_key]

                worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(total),style=yellow_style_title)
                new_col+=1
                worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(total_recovery),style=yellow_style_title)
                new_col+=1

            if select_by_monthly_list:
                worksheet.write_merge(new_row,new_row,new_col,new_col,format_with_commas(final_total), style=yellow_style_title)
                worksheet.write_merge(new_row,new_row,new_col+1,new_col+1,format_with_commas(final_recovery), style=yellow_style_title)
                if final_total>0 and final_recovery>0:
                    final_total_per =(final_recovery/final_total)*100
                    worksheet.write_merge(new_row,new_row,new_col+2,new_col+2,str(round(final_total_per, 4))+' %',style=yellow_style_title)
                           


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
        