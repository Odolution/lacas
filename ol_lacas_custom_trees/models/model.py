
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
import json

class ext(models.Model):
    _inherit="account.move"
    # security_price=fields.Integer(string='Security Price')
   
    tuition=fields.Integer(string="Tuition Fee")
    club=fields.Integer(string="Club Charges")
    computer=fields.Integer(string="computer Charges")
    library=fields.Integer(string="library Charges")
    utility=fields.Integer(string="utility Charges")
    student_code=fields.Char(string="UDID")
    student_name=fields.Char(string="Name")
    class_name=fields.Char(string="Class")
    section_name=fields.Char(string="Section")
    campus=fields.Char(string="Campus")
    bill_date=fields.Char(string="Bill Date")
    due_date=fields.Char(string="Due Date")
    due_amount=fields.Integer(string="Due Amount")
    std_bill_date=fields.Char(string="Issue Date")
    std_due_date=fields.Char(string="Due Date")
    std_branch=fields.Char(string="Branch")
    std_dob=fields.Char(string="Date of Birth")
    std_name=fields.Char(string="Student")
    std_batch=fields.Char(string="Batch")
    std_discount=fields.Char(string="Discount note")
    std_reason=fields.Char(string="Concession Name")
    std_fathername=fields.Char(string="Father Name")
    std_contactno=fields.Char(string="Contact No.")
    adm_amount=fields.Char(string="Admission Amount")
    security_amount=fields.Char(string="Security Amount")
    bill_amount=fields.Char(string="Bill Amount")
    std_factsid=fields.Char(string="Facts ID")
    std_payment_date=fields.Char(string='Payment Date')


    

    def get_charges_action(self):
        action = self.env.ref('ol_lacas_custom_trees.act_account_move_charges').read()[0]
        journals=self.env["account.journal"].search([("name","=","Charges")])
        domain = [('journal_id','in',[i.id for i in journals])]
        action['domain'] = domain
        return action    
    def get_admission_action(self):
        action = self.env.ref('ol_lacas_custom_trees.act_account_move_admission').read()[0]
        journals=self.env["account.journal"].search([("name","=","Admission Challan")])
        domain = [('journal_id','in',[i.id for i in journals])]
        action['domain'] = domain
        return action  

    def get_monthlyBill_action(self):
        action = self.env.ref('ol_lacas_custom_trees.act_account_move_monthlyBill').read()[0]
        journals=self.env["account.journal"].search([("name","=","Monthly Bills")])
        domain = [('journal_id','in',[i.id for i in journals])]
        action['domain'] = domain
        return action  




    @api.onchange('x_student_id_cred',"student_ids")
    def _students_onchange(self):
        self.student_name=''
        self.student_code=" "
        self.campus=""
        self.bill_date=' '
        self.due_date=' '
        self.due_amount=0
        self.tuition=0
        self.club=0
        self.computer=0
        self.library=0
        self.utility=0
        self.class_name=""
        self.std_bill_date=""
        self.std_due_date=""
        self.std_branch=' '
        self.std_dob=' '
        self.std_name=""
        self.std_batch=""
        self.std_discount=""
        self.std_reason=""
        self.std_fathername=""
        self.std_contactno=""
        self.adm_amount=""
        self.security_amount=""
        self.bill_amount=""
        self.std_factsid=""
        self.std_payment_date=""
        self.section_name=""
        if self.student_ids:
            full_name=self.student_ids.first_name+" "+self.student_ids.last_name
            self.student_name=full_name
            self.student_code=self.student_ids.facts_udid
            # self.campus=self.student_ids.school_ids.name
            # self.bill_date=self.invoice_date
            self.due_date=self.invoice_date_due
            self.due_amount=self.due_amount
            self.std_name=full_name
        
            self.std_bill_date=self.invoice_date
            self.std_due_date=self.invoice_date_due
            self.std_discount=self.discount_note
            self.std_reason=self.reject_reason.name
            self.std_batch=self.x_studio_batch.x_name
            self.std_dob=self.student_ids.date_of_birth
            self.std_fathername=self.partner_id.name
            self.std_factsid=self.student_ids.facts_id
            self.std_contactno=self.partner_id.mobile
            self.bill_amount=self.amount_total
            
        
            

            wholename=""
            if self.student_ids.homeroom:
                wholename=self.student_ids.homeroom
                splitted_name=wholename.split('-')
                if len(splitted_name)>2:
                    self.class_name=splitted_name[0]+"-"+splitted_name[1]
                    self.section_name=splitted_name[2]
                elif len(splitted_name)>1:
                    self.class_name=splitted_name[0]
                    self.section_name=splitted_name[1]
                elif len(splitted_name)>0:
                        self.class_name=splitted_name[0]
            wholedate=str(self.invoice_date)
            splitted_name=wholedate.split('-')
            if len(splitted_name)>2:
                month=splitted_name[1]
                wholeyear=splitted_name[0]
                year=wholeyear[2:4]
                if month =='01':
                    self.bill_date="Jan"+"-"+year
                elif month =='02':
                    self.bill_date="Feb"+"-"+year
                elif month =='03':
                    self.bill_date="Mar"+"-"+year
                elif month =='04':
                    self.bill_date="Apr"+"-"+year
                elif month =='05':
                    self.bill_date="May"+"-"+year
                elif month =='06':
                    self.bill_date="Jun"+"-"+year
                elif month =='07':
                    self.bill_date="Jul"+"-"+year
                elif month =='08':
                    self.bill_date="Aug"+"-"+year
                elif month =='09':
                    self.bill_date="Sep"+"-"+year
                elif month =='10':
                    self.bill_date="Oct"+"-"+year
                elif month =='11':
                    self.bill_date="Nov"+"-"+year
                elif month =='12':
                    self.bill_date="Dec"+"-"+year
                
    
            if self.invoice_line_ids: 
                    for line in self.invoice_line_ids:
                        if 'Tuition Fee' in line.product_id.name:
                             self.tuition=line.price_subtotal
                        elif 'Club' in line.product_id.name:
                            self.club=line.price_subtotal
                        elif 'Computer' in line.product_id.name:
                            self.computer=line.price_subtotal
                        elif 'Library' in line.product_id.name:
                            self.library=line.price_subtotal
                        elif 'Utility' in line.product_id.name:
                            self.utility=line.price_subtotal
                        if 'Admission' in line.product_id.name:
                            self.adm_amount=line.price_subtotal
                        elif 'Security' in line.product_id.name:
                           self.security_amount=line.price_subtotal
            if self.payment_state=="paid":
                var=str(json.loads(self.invoice_payments_widget)["content"][-1]["date"])
                self.std_payment_date=var
                

            if self.student_ids.school_ids:
                if self.student_ids.enrollment_history_ids:
                    enroll_history=self.student_ids.enrollment_history_ids
                    lst=[]
                    for lines in enroll_history:
                        lst.append(lines.program_id.name)
                    self.campus=lst[0]
               
            
            
                
                        
        

        
               
    



            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            


                        
                    
            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            

