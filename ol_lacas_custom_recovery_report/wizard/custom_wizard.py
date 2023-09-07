
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



class billingMonthModel(models.Model):
    _name = 'billing.month'
    _description = 'Billing Month Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

class AccountMoveReport(models.TransientModel):
    _name = 'account.recovery.report.move.line'
    
    billing_cycle=fields.Char('Billing Cycle')
    total_issuance=fields.Integer('Total Billing (Bills Issuance)')
    no_of_std=fields.Integer('#No of Students')
    total_recovery=fields.Integer('Recovery')
    recovery_percentage=fields.Char('Percentage of Recovery on Amount')

class ByAccountMoveReport(models.TransientModel):
    _name = 'by.account.recovery.report.move.line'
    
    billing_cycle=fields.Char('Billing Cycle')
    total_issuance=fields.Integer('Total Billing (Bills Issuance)')
    no_of_std=fields.Integer('#No of Students')
    total_recovery=fields.Integer('Recovery')
    recovery_percentage=fields.Char('Percentage of Recovery on Amount')


class RecoveryReportWizard(models.TransientModel):
    _name="recovery.report.wizard"
    _description='Print Recovery Wizard'

    # selected_month= fields.Many2many('billing.month', string='Select Month')
    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    all_branch=fields.Boolean(string=" Select All Branches")
    one_branch=fields.Many2one('school.school', string= 'Select any one branch')

    account_recovery_report_line=fields.Many2many('account.recovery.report.move.line', string='Account report Line')
    by_account_recovery_report_line=fields.Many2many('by.account.recovery.report.move.line', string='Account report Line for By Monthly')
    # groups_ids = fields.Many2many('aging.invoice.group', string='Groups')

    def _branch_constrains(self):

        if self.all_branch and self.one_branch:
            raise ValidationError(_('Sorry, You Must select only one option.'))
             
        elif not self.one_branch and not self.all_branch:
            raise ValidationError(_('Sorry, You Must select atleast one option.'))

        if not self.to_date or not self.from_date:
            raise ValidationError(_('Please Select the both dates.'))

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

        

  
    
    def action_print_report(self):
        lines=[]
        new_lines=[]

        selected_month = self.list_months()
        # raise UserError(selected_month)
        for month in selected_month:
            if self.all_branch==True:
                inv_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('journal_id','=',125),('state','=','posted'),('invoice_date',">=",self.from_date),('invoice_date',"<=",self.to_date)])
            else:
                inv_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('journal_id','=',125),('x_studio_current_branchschool','=',self.one_branch.id),('invoice_date',">=",self.from_date),('invoice_date',"<=",self.to_date)])
            
            stud_lst=[]
            month_issuance=0
            month_due_amount=0
            month_recovery=0
            perc=0
        
            for rec in inv_ids:
                invoice_month = rec.invoice_date.strftime("%b-%y")
                if invoice_month==month:
                    if rec.x_studio_udid_monthly_bills not in stud_lst:
                        stud_lst.append(rec.x_studio_udid_monthly_bills)
                
                    month_issuance=month_issuance+rec.amount_total

                    if rec.payment_state=='paid':
                        month_recovery = month_recovery+rec.amount_total
                
            nostd=len(stud_lst)   
            if month_issuance !=0 :
                number=(month_recovery/month_issuance)*100
                perc = round(number, 2)             

            mvl=self.env['account.recovery.report.move.line'].create({
                                
                                "billing_cycle":month,
                                "total_issuance":month_issuance,
                                "no_of_std":nostd,
                                "total_recovery":month_recovery,
                                "recovery_percentage":str(perc)+'%',
                                


                    })
            lines.append(mvl.id)


            self.write({
                "account_recovery_report_line":[(6,0,lines)]
            })


        # lst = ["Sep-22","Oct-22", "Nov-22", "Dec-22", "Jan-23", "Feb-23", "Mar-23"]

        combinations = []

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
                    combinations.append(f"{months[i]}-{months[j]}-{year}")

        
        if self.all_branch==True:
            for_by_month_inv_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('journal_id','=',126),('state','=','posted'),('invoice_date',">=",self.from_date),('invoice_date',"<=",self.to_date)])
        else:
            for_by_month_inv_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('journal_id','=',126),('x_studio_current_branchschool','=',self.one_branch.id),('invoice_date',">=",self.from_date),('invoice_date',"<=",self.to_date)])
        
        # raise UserError(len(for_by_month_inv_ids))
         
        total_list = [] 
        # a = ""
        month_dict = {"January": 1,"Jan": 1,"February": 2,"Feb": 2,"March": 3,"Mar": 3,"April": 4,"Apr": 4,"May": 5,"June": 6,"Jun": 6,"July": 7,"Jul": 7,"August": 8,"Aug": 8,"September": 9,"Sep": 9,"October": 10,"Oct": 10,"November": 11,"Nov": 11,"December": 12,"Dec": 12}
        months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        # short_month_names = [month[:3] for month in months_list]

        date_str = selected_month[0]
        month, year = date_str.split('-')
        start = month_dict.get(month.capitalize())

        date_str = selected_month[len(selected_month)-1]
        month_last, year_last = date_str.split('-')
        end = month_dict.get(month_last.capitalize())
        # raise UserError(str(start)+" "+str(end))
        
        for item in combinations:
        
            scan_data_list = []
            by_month_issuance=0
            by_month_recovery=0
            by_perc=0

            for rec in for_by_month_inv_ids:
                # a += str(rec.bill_date)+"\n"
                month_start1 , month_end1, and_year1 = item.split('-')
                condition1 = str(month_dict.get(month_start1.capitalize()))+"-"+str(month_dict.get(month_end1.capitalize()))+"-"+and_year1

                try:
                    month_start, month_end, and_year = rec.bill_date.split('-')
                except ValueError:
                condition2 = str(month_dict.get(month_start.capitalize())) +"-"+str(month_dict.get(month_end.capitalize()))+"-"+and_year

                if condition1 == condition2:
                    # raise UserError(str(condition1)+"   "+str(rec.bill_date))
                    if rec.x_studio_udid_monthly_bills not in scan_data_list:
                        scan_data_list.append(rec.x_studio_udid_monthly_bills)
        
                    by_month_issuance += float(rec.net_amount)

                    if rec.payment_state=='paid':
                        by_month_recovery += float(rec.net_amount)

            if by_month_issuance!=0:
                by_nostd=len(scan_data_list)   
                if by_month_issuance !=0 :
                    by_number=(by_month_recovery/by_month_issuance)*100
                    by_perc = round(by_number, 2)
                
                # short_month = short_month_names[i]+"-"+short_month_names[j]+"-"+year_last
                
                by_line=self.env['by.account.recovery.report.move.line'].create({        
                            "billing_cycle":item,
                            "total_issuance":by_month_issuance,
                            "no_of_std":by_nostd,
                            "total_recovery":by_month_recovery,
                            "recovery_percentage":str(by_perc)+'%',
                })
                new_lines.append(by_line.id)


                self.write({
                    "by_account_recovery_report_line":[(6,0,new_lines)]
                })
            # a+=condition1+" : "+str(by_month_issuance)+"  =="+str(by_month_recovery)+"\n"
        
    # raise UserError(month_issuance2)
        # if rec.bi_monthly_cycle == "June-July":
        
    # raise UserError(a)

    def action_print_excel_recovery_report(self):
        
        self._branch_constrains()
      
        self.action_print_report()
        if xlwt:
            branch=""
            if self.all_branch:
                branch="All Branches"
            else:
                branch=self.one_branch.name

            
            filename = str(branch)+"-"+str(self.from_date)+"-"+str(self.to_date)+".xls"
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('Recovery Report')
            

            
            style_title = xlwt.easyxf(
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            red_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour pale_blue;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            yellow_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            lime_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour lime;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")

            grand_heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;'
                              'font: colour black, bold True;')

            heading_style = xlwt.easyxf('align: vertical center,horiz center;')
            
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'dd/mm/yyyy'

            # worksheet.write_merge(0, 1, 0, 5,"LACAS SCHOOL NETWORK ",style=style_title)
            # worksheet.write_merge(0, 1, 6, 11, "Billing Cycle wise recovery report", style=style_title)
            
            

            worksheet.write_merge(0,1,0,2,"Billing Cycle.", style=red_style_title)
            worksheet.write_merge(0,1,3,5,"Total Billing (Bills Issuance)",style=red_style_title)
            worksheet.write_merge(0,1,6,8,"No of Std",style=red_style_title)
            worksheet.write_merge(0,1,9,11,"Recovery",style=red_style_title)
            worksheet.write_merge(0,1,12,15,"Percentage of Recovery on Amount",style=red_style_title)
     
      

            row=2
            for rec in self.account_recovery_report_line:
                if rec:
            
                    worksheet.write_merge(row,row,0,2,rec.billing_cycle, style=style_title)
                    worksheet.write_merge(row,row,3,5,rec.total_issuance,style=style_title)
                    worksheet.write_merge(row,row,6,8,rec.no_of_std,style=style_title)
                    worksheet.write_merge(row,row,9,11,rec.total_recovery,style=style_title)
                    worksheet.write_merge(row,row,12,15,rec.recovery_percentage,style=style_title)
   
                    row+=1
            
            for rec in self.by_account_recovery_report_line:
                if rec:
            
                    worksheet.write_merge(row,row,0,2,rec.billing_cycle, style=style_title)
                    worksheet.write_merge(row,row,3,5,rec.total_issuance,style=style_title)
                    worksheet.write_merge(row,row,6,8,rec.no_of_std,style=style_title)
                    worksheet.write_merge(row,row,9,11,rec.total_recovery,style=style_title)
                    worksheet.write_merge(row,row,12,15,rec.recovery_percentage,style=style_title)
   
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