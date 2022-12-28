
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
import json





class ext(models.Model):
    _inherit="account.move"

    month_date=fields.Char(string="Month",compute="_get_month_date")
    month_total=fields.Char(string="Month Total",compute="_get_month_date")
    
    def _get_month_date(self):
        self.month_date=''
        for rec in self:
            if rec.move_type=="out_refund":
                due_date=str(rec.invoice_date)
                splitted_name=due_date.split('-')
                if len(splitted_name)>2:
                    month_in_number=splitted_name[1]
                    if month_in_number == '12':
                        rec['month_date']='December'
                    elif month_in_number == '11':
                        rec['month_date']='November'
                    elif month_in_number == '10':
                        rec['month_date']='October'
                    elif month_in_number == '09':
                        rec['month_date']='September'
                    elif month_in_number == '08':
                        rec['month_date']='August'
                    elif month_in_number == '07':
                        rec['month_date']='July'
                    elif month_in_number == '06':
                        rec['month_date']='June'
                    elif month_in_number == '05':
                        rec['month_date']='May'
                    elif month_in_number == '04':
                        rec['month_date']='April'
                    elif month_in_number == '03':
                        rec['month_date']='March'
                    elif month_in_number == '02':
                        rec['month_date']='Feburary'
                    elif month_in_number == '01':
                        rec['month_date']='January'
        
    # def _get_monthly_total(self):
    #     for rec in self:

    #         if rec.move_type=="out_refund":

                    
                        
        


                

                       
        
        



#     # security_price=fields.Integer(string='Security Price')
   
#     tuition=fields.Integer(string="Tuition Fee", compute='_onchange_tuition')
#     club=fields.Integer(string="Club Charges", compute="_onchange_club")
#     computer=fields.Integer(string="computer Charges", compute="_onchange_computer")
#     library=fields.Integer(string="library Charges", compute="_onchange_library")
#     utility=fields.Integer(string="utility Charges", compute="_onchange_utility")
#     student_code=fields.Integer(string="Student Code",compute="_onchange_student_code_data")
#     student_name=fields.Char(string="Name",compute="_onchange_student_name_data")
#     class_mnt=fields.Char(string="Section",compute="_onchange_class_sec_data")
#     sec_mnt=fields.Char(string="Section",compute="_onchange_sec_data")
#     campus=fields.Char(string="Campus",compute="_onchange_campus_data")
#     bill_date=fields.Char(string="Bill Date",compute="_onchange_bill_date_data")
#     due_date=fields.Char(string="Due Date",compute="_onchange_due_date_data")
#     due_amount=fields.Integer(string="Due Amount",compute="_onchange_due_amount_data")

#     std_udid=fields.Integer(string="UDID",compute="_onchange_udid_data")
#     std_class=fields.Char(string="Class",compute="_onchange_class_data")
#     std_bill_date=fields.Date(string="Issue Date",compute="_onchange_std_bill_date_data")
#     std_due_date=fields.Date(string="Due Date",compute="_onchange_std_due_date_data")
#     std_branch=fields.Char(string="Branch",compute="_onchange_branch_data")
#     std_dob=fields.Char(string="Date of Birth",compute="_onchange_dob_data")
#     std_name=fields.Char(string="Student",compute="_onchange_std_name_data")
#     std_batch=fields.Char(string="Batch",compute="_onchange_batch_data")
#     std_discount=fields.Char(string="Discount note",compute="_onchange_std_discount_data")
#     std_reason=fields.Char(string="Concession Name",compute="_onchange_std_reason_data")
#     std_fathername=fields.Char(string="Father Name",compute="_onchange_std_fathername_data")
#     std_contactno=fields.Char(string="Contact No.",compute="_onchange_std_contactno_data")

#     adm_amount=fields.Char(string="Admission Amount",compute="_onchange_adm_amount_data")
#     security_amount=fields.Char(string="Security Amount",compute="_onchange_security_amount_data")
#     bill_amount=fields.Char(string="Bill Amount",compute="_onchange_bill_amount_data")
#     std_factsid=fields.Integer(string="Facts ID",compute="_onchange_facts_id_data")
#     ol_payment_date = fields.Date(string='Payment Date')
    




#     def get_charges_action(self):
#         action = self.env.ref('ol_lacas_custom_trees.act_account_move_charges').read()[0]
#         journals=self.env["account.journal"].search([("name","=","Charges")])
#         domain = [('journal_id','in',[i.id for i in journals])]
#         action['domain'] = domain
#         return action    
#     def get_admission_action(self):
#         action = self.env.ref('ol_lacas_custom_trees.act_account_move_admission').read()[0]
#         journals=self.env["account.journal"].search([("name","=","Admission")])
#         domain = [('journal_id','in',[i.id for i in journals])]
#         action['domain'] = domain
#         return action  

#     def get_monthlyBill_action(self):
#         action = self.env.ref('ol_lacas_custom_trees.act_account_move_monthlyBill').read()[0]
#         journals=self.env["account.journal"].search([("name","=","Monthly bills")])
#         domain = [('journal_id','in',[i.id for i in journals])]
#         action['domain'] = domain
#         return action  
    
#     def get_securityDeposit_action(self):
#         action = self.env.ref('ol_lacas_custom_trees.act_account_move_securityDeposit').read()[0]
#         journals=self.env["account.journal"].search([("name","=","Security")])
#         domain = [('journal_id','in',[i.id for i in journals])]
#         action['domain'] = domain
#         return action  



# #monthly_bills 
    
#     @api.onchange('invoice_line_ids')
#     def _onchange_tuition(self):
#         self._get_price_field()

#     @api.onchange('invoice_line_ids')
#     def _onchange_club(self):
#         self._get_club_field()

#     @api.onchange('invoice_line_ids')
#     def _onchange_computer(self):
#         self._get_computer_field()

#     @api.onchange('invoice_line_ids')
#     def _onchange_library(self):
#         self._get_library_field()

#     @api.onchange('invoice_line_ids')
#     def _onchange_utility(self):
#         self._get_utility_field()

#     @api.onchange('student_ids')
#     def _onchange_student_name_data(self):
#         self._get_student_name_field()
    
#     @api.onchange('student_ids')
#     def _onchange_student_code_data(self):
#         self._get_student_code_field()
    
#     @api.onchange('student_ids')
#     def _onchange_sec_data(self):
#         self._get_sec_field()
    
#     @api.onchange('student_ids')
#     def _onchange_class_data(self):
#         self._get_class_field()


#     @api.onchange('student_ids')
#     def _onchange_campus_data(self):
#         self._get_campus_field()
    
    
#     @api.onchange('student_ids')
#     def _onchange_bill_date_data(self):
#         self._get_bill_date_field()

#     @api.onchange('student_ids')
#     def _onchange_due_date_data(self):
#         self._get_due_date_field()

    
#     @api.onchange('student_ids')
#     def _onchange_due_amount_data(self):
#         self._get_due_amount_field()
    
    

    
        
       

#     def _get_student_name_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         for rec in monthly_bill:
#             if rec.student_ids:
#                 full_name=rec.student_ids.first_name+" "+rec.student_ids.last_name
#                 rec['student_name']=full_name


#     def _get_student_code_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         for rec in monthly_bill:
#             if rec.student_ids:
#                 rec['student_code']=rec.student_ids.facts_udid
    
#     def _get_class_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         self.class_mnt=' '
#         for rec in monthly_bill:
#             if rec.student_ids.homeroom:
                
#                 classnsec=rec.student_ids.homeroom
#                 splitted_name=classnsec.split('-')
#                 if len(splitted_name)>2:
#                     rec.class_mnt=splitted_name[0]+"-"+splitted_name[1]
#                     # rec.std_sec=splitted_name[2]
#                 elif len(splitted_name)>1:
#                     rec.class_mnt=splitted_name[0]
#                     # rec.std_sec=splitted_name[1]
#                 elif len(splitted_name)>0:
#                     rec.class_mnt=splitted_name[0]

#     def _get_sec_field(self):
#             monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#             monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#             self.sec_mnt=' '
#             for rec in monthly_bill:
#                 if rec.student_ids.homeroom:
#                     classnsec=rec.student_ids.homeroom
#                     splitted_name=classnsec.split('-')
#                     if len(splitted_name)>2:
                        
#                         rec.sec_mnt=splitted_name[2]
#                     elif len(splitted_name)>1:
                       
#                         rec.sec_mnt=splitted_name[1]
                  
#     def _get_campus_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         for rec in monthly_bill:
#             if rec.student_ids:
#                 rec['campus']=rec.student_ids.school_ids.name
                

#     def _get_bill_date_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         for rec in monthly_bill:
#             if rec.student_ids:
#                 rec['bill_date']=rec.invoice_date
                
    
#     def _get_due_date_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         for rec in monthly_bill:
#             if rec.student_ids:
#                 rec['due_date']=rec.invoice_date_due
#     def _get_due_amount_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         for rec in monthly_bill:
#             if rec.student_ids:
#                 rec['due_date']=rec.due_amount
   


                



        



#     def _get_price_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         self.tuition=0
#         for rec in monthly_bill:
#                 if rec.invoice_line_ids: 
#                     for line in rec.invoice_line_ids:
#                         if 'Tuition Fee' in line.product_id.name:
#                             rec['tuition']=line.price_subtotal
                        

#     def _get_club_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         self.club=0
#         for rec in monthly_bill:
#                 if rec.invoice_line_ids: 
#                     for line in rec.invoice_line_ids:
#                         if 'Club' in line.product_id.name:
#                             rec['club']=line.price_subtotal
                        

#     def _get_computer_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         self.computer=0
#         for rec in monthly_bill:
#                 if rec.invoice_line_ids: 
#                     for line in rec.invoice_line_ids:
#                         if 'Computer' in line.product_id.name:
#                             rec['computer']=line.price_subtotal
                       

#     def _get_library_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         self.library=0
#         for rec in monthly_bill:
#                 if rec.invoice_line_ids: 
#                     for line in rec.invoice_line_ids:
#                         if 'Library' in line.product_id.name:
#                             rec['library']=line.price_subtotal
                
#     def _get_utility_field(self):
#         monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
#         monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
#         self.utility=0
#         for rec in monthly_bill:
#                 if rec.invoice_line_ids: 
#                     for line in rec.invoice_line_ids:
#                         if 'Utility' in line.product_id.name:
#                             rec['utility']=line.price_subtotal
                    

# #admission


    
#     @api.onchange('student_ids')
#     def _onchange_std_name_data(self):
#         self._get_std_name_field()

#     def _get_std_name_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_name=''
        
#         for rec in adm_journals:
            
#             if rec.student_ids:
#                 full_name=rec.student_ids.first_name+" "+rec.student_ids.last_name
#                 rec['std_name']=full_name

    
#     @api.onchange('student_ids')
#     def _onchange_dob_data(self):
#         self._get_dob_field()
    
                
#     def _get_dob_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_dob=' '
#         for rec in adm_journals:

#             rec.std_dob=' '
#             if rec.student_ids:
#                 rec['std_dob']=rec.student_ids.date_of_birth
    

 
    
#     @api.onchange('student_ids')
#     def _onchange_udid_data(self):
#         self._get_udid_field()
    
                
#     def _get_udid_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_udid=0
#         for rec in adm_journals:

           
#             if rec.student_ids:
#                 rec['std_udid']=rec.student_ids.facts_udid

   
#     @api.onchange('student_ids')
#     def _onchange_facts_id_data(self):
#         self._get_facts_id_field()
    
                
#     def _get_facts_id_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_factsid=''
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_factsid']=rec.student_ids.facts_id

#     @api.onchange('invoice_line_ids')
#     def _onchange_adm_amount_data(self):
#         self._get_adm_amt_field()
    
                
#     def _get_adm_amt_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.adm_amount=0
#         for rec in adm_journals:
#             if rec.invoice_line_ids: 
#                     for line in rec.invoice_line_ids:
#                         if 'Admission' in line.product_id.name:
#                             rec['adm_amount']=line.price_subtotal

#     @api.onchange('invoice_line_ids')
#     def _onchange_security_amount_data(self):
#         self._get_sec_amt_field()
    
                
#     def _get_sec_amt_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.security_amount=''
#         for rec in adm_journals:
#              if rec.invoice_line_ids: 
#                     for line in rec.invoice_line_ids:
#                         if 'Security' in line.product_id.name:
#                             rec['security_amount']=line.price_subtotal

#     @api.onchange('invoice_line_ids')
#     def _onchange_bill_amount_data(self):
#         self._get_sec_bill_field()
    
                
#     def _get_sec_bill_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.bill_amount=''
#         for rec in adm_journals:
#             rec['bill_amount']=rec.tax_totals_json[16:24]

             



#     @api.onchange('student_ids')
#     def _onchange_std_discount_data(self):
#         self._get_std_discount_field()
    
                
#     def _get_std_discount_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_discount=''
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_discount']=rec.discount_note
    
#     @api.onchange('student_ids')
#     def _onchange_std_reason_data(self):
#         self._get_std_reason_field()
    
                
#     def _get_std_reason_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_reason=''
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_reason']=rec.reject_reason
    
    

#     @api.onchange('student_ids')
#     def _onchange_batch_data(self):
#         self._get_batch_field()
    
                
#     def _get_batch_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_batch=''
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_batch']=rec.x_studio_batch
    
    
#     @api.onchange('student_ids')
#     def _onchange_class_data(self):
#         self._get_class_field()

    
    
   
#     @api.onchange('student_ids')
#     def _onchange_std_fathername_data(self):
#         self._get_father_field()

    
#     def _get_father_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_fathername=' '
#         for rec in adm_journals:
#             if rec.student_ids:

#                 rec['std_fathername']=rec.partner_id.name

#     @api.onchange('student_ids')
#     def _onchange_std_contactno_data(self):
#         self._get_contactno_field()

    
#     def _get_contactno_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_contactno=' '
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_contactno']=rec.partner_id.mobile


    
    
#     @api.onchange('student_ids')
#     def _onchange_branch_data(self):
#         self._get_branch_field()

#     def _get_branch_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_branch=' '
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_branch']=rec.student_ids.school_ids.name
                
    
    
#     @api.onchange('student_ids')
#     def _onchange_std_bill_date_data(self):
#         self._get_std_bill_date_field()

#     def _get_std_bill_date_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_bill_date=' '
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_bill_date']=rec.invoice_date

#     @api.onchange('student_ids')
#     def _onchange_std_due_date_data(self):
#         self._get_std_due_date_field()

#     def _get_std_due_date_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_due_date=' '
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_due_date']=rec.invoice_date_due 

#     def _get_class_field(self):
#         adm_journal=self.env['account.journal'].search([('code','=','ADM')])
#         adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
#         self.std_class=' '
#         for rec in adm_journals:
#             if rec.student_ids:
#                 rec['std_due_date']=rec.grade_level_ids.name 







   


                    
   
                    

                    


                    
                

                 
            

