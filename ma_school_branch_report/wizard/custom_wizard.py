
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

import xlsxwriter
_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


import base64

import io
try:
    import xlwt
except ImportError:
    xlwt = None



class AccountMoveReport(models.TransientModel):
    _name = 'student.report.line'
    
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

    def action_print_report(self):
        lines=[]
        school_ids = []
        billing_list=[]
        billing_list_paid=[]
        global billing_counts
        billing_counts = {}

        school_ids_raw=self.env['school.school'].search([])
        school_ids_raw = school_ids_raw.sorted(lambda o : o.name)

        v_from_month=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%m')
        v_from_year=datetime.strptime(str(self.from_date), "%Y-%m-%d").strftime('%y')

        v_to_month=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%m')
        v_to_year=datetime.strptime(str(self.to_date), "%Y-%m-%d").strftime('%y')

        pay_from_month=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%m')
        pay_from_year=datetime.strptime(str(self.from_date_pay), "%Y-%m-%d").strftime('%y')

        pay_to_month=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%m')
        pay_to_year=datetime.strptime(str(self.to_date_pay), "%Y-%m-%d").strftime('%y')

        for rec in school_ids_raw:
            school_ids.append(rec)
            # raise UserError(rec.program_ids)
           
            school_bill_ids = self.env['account.move'].search([
                ('program_ids', 'in', rec.program_ids.ids),
                ('state', '=', 'posted')
            ])
            
            total_count=0
            total_count_paid=0
            for bill_rec in school_bill_ids:
                invoice_date = bill_rec.invoice_date
                month_in_invoice = invoice_date.strftime('%m')
                year_in_invoice = invoice_date.strftime('%y')
                
                # Check if the invoice date is within the specified range
                if v_from_year <= year_in_invoice <= v_to_year and v_from_month <= month_in_invoice <= v_to_month:
                    # Create a key using the month and year
                    month_key = f"{rec.name}-{year_in_invoice}-{month_in_invoice}"
                    
                    if bill_rec.payment_state =="paid":
                        if bill_rec.ol_payment_date:
                            payment_date = bill_rec.ol_payment_date
                            month_in_payment = payment_date.strftime('%m')
                            year_in_payment = payment_date.strftime('%y')

                            if pay_from_year <= year_in_payment <= pay_to_year and pay_from_month <= month_in_payment <= pay_to_month:
                                total_count_paid += float(bill_rec.net_amount)

                    if month_key in billing_counts:
                        billing_counts[month_key] += float(bill_rec.net_amount)
                        total_count += float(bill_rec.net_amount)
                    else:
                        billing_counts[month_key] = float(bill_rec.net_amount)
                        total_count += float(bill_rec.net_amount)

            billing_list_paid.append(total_count_paid)
            billing_list.append(total_count)

            for year in range(int(v_from_year), int(v_to_year) + 1):
                for month in range(int(v_from_month), int(v_to_month) + 1):
                    month_key = f"{rec.name}-{str(year)[-2:]}-{month:02}"
                    if month_key not in billing_counts:
                        billing_counts[month_key] = 0
           
            # raise UserError(billing_counts)

        # message = "Billing information:\n\n"
        # for month_key, count in billing_counts.items():
        #     # month_key format: 'yy-mm'
        #     message += f"Month: {month_key}, Number of bills: {count}\n"
            
        # # Raise a UserError with the summarized message
        # raise UserError(message)
        

        for item in range(len(school_ids)):
            mvl=self.env['student.report.line'].create({
                                        
                "branch_name":school_ids[item].name,
                "school_bill_len":billing_list[item],
                "billing_list_paid":billing_list_paid[item],
            })
            lines.append(mvl.id)


        self.write({
            "account_report_line":[(6,0,lines)]
        })  
        # raise UserError(school_ids.name)

    def action_print_excel_school_branch_report(self):
        
        

        self.action_print_report()
        
        
        if xlwt:
            global billing_counts
            
            filename = 'Students Branch Report.xls'
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('Students Branch Std')
            

            
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
                }
            range_start = 0
            range_stop = 0
            # raise UserError(v_to)
            for key, value in months.items():
                if value[0] == v_from_month and value[3] == v_from_year:
                    range_start = key
                if value[0] == v_to_month and value[3] == v_to_year:

                    range_stop = key

            worksheet.write_merge(0,1,0,3,"Current Branch/School", style=red_style_title)
            # worksheet.write_merge(0,1,4,5,"Billing month Jul-23",style=red_style_title)
            
            
            col = 4
            
            # raise UserError(str(range_start)+" "+str(range_stop))
      
            for i in range(range_start,range_stop+1):
                # raise UserError(months[i][0]+" "+months[i][3])
                worksheet.write_merge(0,1,col,col+2,'Billing month '+months[i][1],red_style_title)
                # worksheet.write_merge(row,row,col,col+1,months[i][2])
                col+=3
             
            worksheet.write_merge(0,1,col,col+1,"Total",style=red_style_title)
            worksheet.write_merge(0,1,col+2,col+4,"Branch Wise Recovery",style=red_style_title)
            worksheet.write_merge(0,1,col+5,col+6,"'%' age of Recovery",style=yellow_style_title)
            # worksheet.write_merge(2,3,col,col+1,"Total", lime_style_title)   
            
                # print('col:',months[i][1], 'data:',months[i][2])
            group_total=0
            final_total=0
            group_recovery=0
            final_recovery=0
            group_name_list=[]
            months_total_dict={}
            row=2
            col=4
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

                        else:
                            # message = "Billing information:\n\n"
                            # for month_key, count in months_total_dict.items():
                            #     # month_key format: 'yy-mm'
                            #     original_string = month_key
                            #     split_parts = original_string.split('-')
                            #     result = split_parts[0]
                            #     message += f"Month: {result}, Number of bills: {count}\n"
                                
                            # # Raise a UserError with the summarized message
                            # raise UserError(message)
                            col=4
                            for month_key, count in months_total_dict.items():
                                original_string = month_key
                                split_parts = original_string.split('-')
                                result = split_parts[0]
                                if substring == result:
                                    worksheet.write_merge(row,row,col,col+2,count, style=yellow_style_title)
                                    col+=3
                                    
                            worksheet.write_merge(row,row,0,3,"Total", style=yellow_style_title)
                            worksheet.write_merge(row,row,col,col+1,group_total, style=yellow_style_title)
                            worksheet.write_merge(row,row,col+2,col+4,group_recovery, style=yellow_style_title)
                            if group_recovery>0 and group_recovery>0:
                                total_per_new =(group_recovery/group_total)*100
                                worksheet.write_merge(row,row,col+5,col+6,str(round(total_per_new, 4))+' %',style=yellow_style_title)
                            else:
                                worksheet.write_merge(row,row,col+5,col+6,'0 %',style=yellow_style_title)
                            #  raise UserError(str(group_name_list)+"==="+str(group_total)+" =="+str(row))
                            row+=1
                            final_total+=group_total
                            final_recovery+=group_recovery
                            group_name_list.clear()
                            group_total=0
                            group_recovery=0

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
                    # Print row data
                    worksheet.write_merge(row,row,0,3,rec.branch_name, style=style_title)
                    col=4
                    for i in range(range_start,range_stop+1):
                        # check=True
                        new_month_key = f"{rec.branch_name}-{months[i][3]}-{months[i][0]}"
                        for month_key, count in billing_counts.items():
                            if new_month_key==month_key:
                                worksheet.write_merge(row,row,col,col+2,count,style=style_title)
                                # check=False
                            # else:
                            #     worksheet.write_merge(row,row,col,col+2,0,style=style_title)
                        # if check:
                        #     worksheet.write_merge(row,row,col,col+2,0,style=style_title)
                        col+=3
                    # raise UserError(message)
                    worksheet.write_merge(row,row,col,col+1,rec.school_bill_len,style=style_title)
                    worksheet.write_merge(row,row,col+2,col+4,rec.billing_list_paid,style=style_title)
                    if rec.school_bill_len>0 and rec.billing_list_paid>0:
                        total_per =(rec.billing_list_paid/rec.school_bill_len)*100
                        worksheet.write_merge(row,row,col+5,col+6,str(round(total_per, 4))+' %',style=style_title)
                    else:
                        worksheet.write_merge(row,row,col+5,col+6,'0 %',style=style_title)
                    
                    
                            # raise UserError(str(group_name_list)+"==="+str(group_total))
                            # raise UserError(str(group_name_list)+"==="+str(group_total))
                    # worksheet.write_merge(row,row,2,2,rec.no_of_std,style=style_title)
                    # worksheet.write_merge(row,row,3,3,rec.total_recovery,style=style_title)
                    # worksheet.write_merge(row,row,4,4,rec.recovery_percentage,style=style_title)
   
                    row+=1
            # message = "Billing information:\n\n"
            # for month_key, count in months_total_dict.items():
            #     # month_key format: 'yy-mm'
            #     message += f"Month: {month_key}, Number of bills: {count}\n"
                
            # # Raise a UserError with the summarized message
            # raise UserError(message)
            worksheet.write_merge(row,row,0,3,"Total", style=yellow_style_title)

            col=4
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
            
            worksheet.write_merge(row,row,col,col+1,final_total, style=yellow_style_title)
            worksheet.write_merge(row,row,col+2,col+4,final_recovery, style=yellow_style_title)
            if final_total>0 and final_recovery>0:
                final_total_per =(final_recovery/final_total)*100
                worksheet.write_merge(row,row,col+5,col+6,str(round(final_total_per, 4))+' %',style=yellow_style_title)
            
            # message = "Billing information:\n\n"
            # for month_key, count in billing_counts.items():
            #     # month_key format: 'yy-mm'
            #     # worksheet.write_merge(row,row,13,14,count,style=style_title)
            #     message += f"Month: {month_key}, Number of bills: {count}\n"
                
            # # Raise a UserError with the summarized message
            # raise UserError(message)

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
        