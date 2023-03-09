
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
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

# class GroupAging(models.Model):
#     _name = 'aging.invoice.group'

#     name  =  fields.Char(string="Name")
#     grouping = fields.Char('Groups')

class billingMonthModel(models.Model):
    _name = 'billing.month'
    _description = 'Billing Month Model'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

#     @api.model
#     def create(self, vals):
#         values_to_create = [
#     {
#         'name': 'Jan-22',
#         'description': 'This is record 1',
#         #'value': 10.0,
#     },
#     {
#         'name': 'Feb-22',
#         'description': 'This is record 2',
#         #'value': 20.0,
#     },
#     {
#         'name': 'Mar-22',
#         'description': 'This is record 3',
#         #'value': 30.0,
#     },

#        {
#         'name': 'Apr-22',
#         'description': 'This is record 1',
#         #'value': 10.0,
#     },
#     {
#         'name': 'May-22',
#         'description': 'This is record 2',
#         #'value': 20.0,
#     },
#     {
#         'name': 'Jun-22',
#         'description': 'This is record 3',
#         #'value': 30.0,
#     },
#        {
#         'name': 'Jul-22',
#         'description': 'This is record 1',
#         #'value': 10.0,
#     },
#     {
#         'name': 'Aug-22',
#         'description': 'This is record 2',
#         #'value': 20.0,
#     },
#     {
#         'name': 'Sep-22',
#         'description': 'This is record 3',
#         #'value': 30.0,
#     },
#        {
#         'name': 'Oct-22',
#         'description': 'This is record 1',
#         #'value': 10.0,
#     },
#     {
#         'name': 'Nov-22',
#         'description': 'This is record 2',
#         #'value': 20.0,
#     },
#     {
#         'name': 'Dec-22',
#         'description': 'This is record 3',
#         #'value': 30.0,
#     },
#         {
#         'name': 'Jan-23',
#         'description': 'This is record 1',
#         #'value': 10.0,
#     },
#     {
#         'name': 'Feb-23',
#         'description': 'This is record 2',
#         #'value': 20.0,
#     },
#     {
#         'name': 'Mar-23',
#         'description': 'This is record 3',
#         #'value': 30.0,
#     },

#        {
#         'name': 'Apr-23',
#         'description': 'This is record 1',
#         #'value': 10.0,
#     },
#     {
#         'name': 'May-23',
#         'description': 'This is record 2',
#         #'value': 20.0,
#     },
#     {
#         'name': 'Jun-23',
#         'description': 'This is record 3',
#         #'value': 30.0,
#     },
#        {
#         'name': 'Jul-23',
#         'description': 'This is record 1',
#         #'value': 10.0,
#     },
#     {
#         'name': 'Aug-23',
#         'description': 'This is record 2',
#         #'value': 20.0,
#     },
#     {
#         'name': 'Sep-23',
#         'description': 'This is record 3',
#         #'value': 30.0,
#     },
#        {
#         'name': 'Oct-23',
#         'description': 'This is record 1',
#         #'value': 10.0,
#     },
#     {
#         'name': 'Nov-23',
#         'description': 'This is record 2',
#         #'value': 20.0,
#     },
#     {
#         'name': 'Dec-23',
#         'description': 'This is record 3',
#         #'value': 30.0,
#     },
 
# ]
# for values in values_to_create:
#     my_model_obj.create(values)
#         # Add some custom logic when creating a record
#         return super(billingMonthModel, self).create(values_to_create)

# my_model_obj = self.env['billing.month']



class AccountMoveReport(models.TransientModel):
    _name = 'account.recovery.report.move.line'
    
    billing_cycle=fields.Char('Billing Cycle')
    total_issuance=fields.Integer('Total Billing (Bills Issuance)')
    no_of_std=fields.Integer('#No of Students')
    total_recovery=fields.Integer('Recovery')
    recovery_percentage=fields.Char('Percentage of Recovery on Amount')


class RecoveryReportWizard(models.TransientModel):
    _name="recovery.report.wizard"
    _description='Print Recovery Wizard'

    select_month= fields.Many2many('billing.month','name', string= 'Select Month',widget="many2many_tags")
    all_branch=fields.Boolean(string=" Select All Branches")
    one_branch=fields.Many2one('school.program', string= 'Select any one branch')

    account_recovery_report_line=fields.Many2many('account.recovery.report.move.line', string='Account report Line')
    # groups_ids = fields.Many2many('aging.invoice.group', string='Groups')

    def _branch_constrains(self):
        pass

        # if self.all_branch==True and self.one_branch!=False:
        #         raise ValidationError(_('Sorry, You Must select one option...'))
             

        # elif self.one_branch!=False and self.all_branch==True:
        #         raise ValidationError(_('Sorry, You Must select one option...'))

        # if not self.select_month:
        #     raise ValidationError(_('Please Select Billing Month...'))

        

  
    
    def action_print_report(self):
        pass


        # if self.all_branch:
        #     for month in self.select_month:
        #         inv_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('bill_date','=',month)])
        #         lines=[]

                
        #         stud_lst=[]
        #         month_issuance=0
        #         month_recovery=0

            
        #         for rec in inv_ids:
        #             bill_month=rec.bill_date
        #             if rec.student_name not in stud_lst:
        #                 stud_lst.append(rec.student_name)
                
                    
        #             if rec.payment_state=='not_paid':
        #                 month_issuance=month_issuance+rec.amount_residual
                    
        #             if rec.payment_state=='paid':
        #                 if rec.bill_amount:
        #                     month_recovery=month_recovery+int(rec.bill_amount)
        #         nostd=len(stud_lst)    
        #         unpaids=month_issuance
        #         paids=month_recovery
        #         # if paids==0:
        #         #     perc=0
        #         # else:
        #         #     perc=unpaids/paids*100



        #         mvl=self.env['account.recovery.report.move.line'].create({
                                    
        #                             "billing_cycle":bill_month,
        #                             "total_issuance":unpaids,
        #                             "no_of_std":nostd,
        #                             "total_recovery":paids,
        #                             "recovery_percentage":'100'+'%',
                                    


        #                 })
        #         lines.append(mvl.id)


        #         self.write({
        #             "account_recovery_report_line":[(6,0,lines)]
        #         })  

        # else:
        #     selected_campus=self.one_branch.id

        #     for month in self.select_month:
            
        #         inv_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('bill_date','=',month),('campus','=',selected_campus)])
        #         lines=[]

                
        #         stud_lst=[]
        #         month_issuance=0
        #         month_recovery=0

        #         bill_month=self.select_month
        #         for rec in inv_ids:
        #             # bill_month=rec.bill_date
        #             if rec.student_name not in stud_lst:
        #                 stud_lst.append(rec.student_name)
                
                    
        #             if rec.payment_state=='not_paid':
        #                 month_issuance=month_issuance+rec.amount_residual
                    
        #             if rec.payment_state=='paid':
        #                 if rec.bill_amount:
        #                     month_recovery=month_recovery+int(rec.bill_amount)
        #         nostd=len(stud_lst)    
        #         unpaids=month_issuance
        #         paids=month_recovery
        #         # if paids==0:
        #         #     perc=0
        #         # else:
        #         #     perc=unpaids/paids*100



        #         mvl=self.env['account.recovery.report.move.line'].create({
                                    
        #                             "billing_cycle":bill_month,
        #                             "total_issuance":unpaids,
        #                             "no_of_std":nostd,
        #                             "total_recovery":paids,
        #                             "recovery_percentage":'100'+'%',
                                    


        #                 })
        #         lines.append(mvl.id)


        #         self.write({
        #             "account_recovery_report_line":[(6,0,lines)]
        #         })  



    def action_print_excel_recovery_report(self):
        pass
        # self.action_print_report()
        # if xlwt:

            
        #     filename = 'Recovery Report.xls'
        #     # One sheet by partner
        #     workbook = xlwt.Workbook()
        #     # sheet = workbook.add_sheet(report_name[:31])
        #     worksheet = workbook.add_sheet('Recovery Report')
            

            
        #     style_title = xlwt.easyxf(
        #     "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
        #     red_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour pale_blue;'
        #     "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
        #     yellow_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
        #     "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
        #     lime_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour lime;'
        #     "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")

        #     grand_heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;'
        #                       'font: colour black, bold True;')

        #     heading_style = xlwt.easyxf('align: vertical center,horiz center;')
            
        #     date_format = xlwt.XFStyle()
        #     date_format.num_format_str = 'dd/mm/yyyy'

        #     worksheet.write_merge(0, 1, 0, 5,"LACAS SCHOOL NETWORK ",style=style_title)
        #     worksheet.write_merge(0, 1, 6, 11, "Billing Cycle wise recovery report", style=style_title)
            
            

        #     worksheet.write_merge(2,3,0,1,"Billing Cycle.", style=red_style_title)
        #     worksheet.write_merge(2,3,2,4,"Total Billing (Bills Issuance)",style=red_style_title)
        #     worksheet.write_merge(2,3,5,7,"No of Std",style=red_style_title)
        #     worksheet.write_merge(2,3,8,10,"Recovery",style=red_style_title)
        #     worksheet.write_merge(2,3,11,14,"Percentage of Recovery on Amount",style=red_style_title)
     
      

        #     row=4
        #     for rec in self.account_recovery_report_line:
        #         if rec:
            
        #             worksheet.write_merge(row,row,0,1,rec.billing_cycle, style=style_title)
        #             worksheet.write_merge(row,row,2,4,rec.total_issuance,style=style_title)
        #             worksheet.write_merge(row,row,5,7,rec.no_of_std,style=style_title)
        #             worksheet.write_merge(row,row,8,10,rec.total_recovery,style=style_title)
        #             worksheet.write_merge(row,row,11,14,rec.recovery_percentage,style=style_title)
   
        #             row+=1
                  

        #     fp = io.BytesIO()
        #     workbook.save(fp)

        #     export_id = self.env['sale.day.book.report.excel'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        #     res = {
        #             'view_mode': 'form',
        #             'res_id': export_id.id,
        #             'res_model': 'sale.day.book.report.excel',
        #             'type': 'ir.actions.act_window',
        #             'target':'new'
        #         }
        #     return res
            
        # else:
        #     raise Warning (""" You Don't have xlwt library.\n Please install it by executing this command :  sudo pip3 install xlwt""")
        

   
                

           







        
            



















