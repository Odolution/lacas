
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
import json

class ext(models.Model):
    _inherit="account.move"
   
   
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
    bill_date=fields.Char(string="Billing Month")
    challan_date=fields.Char(string="Challan date")
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
    net_amount=fields.Char(string="Net Amount")
    std_factsid=fields.Char(string="Facts ID")
    std_payment_date=fields.Char(string='Payment Date')
    std_tuition_plan=fields.Char(string="Tuition Plan")
    std_tuition_plan_state=fields.Char(string="Tuition Plan State")
    
    art=fields.Integer(string="Art")
    biology=fields.Integer(string="Biology")
    chemistry=fields.Integer(string="Chemistry")
    physics=fields.Integer(string="Physics")
    computing=fields.Integer(string="Computing")
    classphoto=fields.Integer(string="Class Photo")
    collegemagazine=fields.Integer(string="College Magazine")
    dc=fields.Integer(string="Discipline Charges")
    ec=fields.Integer(string="Examination Charges")
    farewell=fields.Integer(string="Farewell")
    gatepass=fields.Integer(string="Gate Pass")
    idcard=fields.Integer(string="ID Card")
    idcardfine=fields.Integer(string="ID Card Fine")
    latecoming=fields.Integer(string="Late Coming")
    latefee=fields.Integer(string="Late Fee")
    libfine=fields.Integer(string="Library Fine")
    mnf=fields.Integer(string="Miscellaneous & Fine")
    mobfine=fields.Integer(string="Mobile Fine")
    news=fields.Integer(string="Newsletter")
    paragon=fields.Integer(string="Paragon 2nd Child and Onwards")
    books=fields.Integer(string="Photocopy (Books)")
    pcopy=fields.Integer(string="Photocopying Charges")
    photo=fields.Integer(string="Photograph")
    scarf=fields.Integer(string="Scarf")
    sportd=fields.Integer(string="Sports Day")
    stationary=fields.Integer(string="Stationary Charges")
    welcome=fields.Integer(string="Wellcome Party")
    workbook=fields.Integer(string="Work Books")
    uniform=fields.Integer(string="Uniform Fine")
    continuation=fields.Integer(string="Continuation")








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

    def get_bimonthlyBill_action(self):
        action = self.env.ref('ol_lacas_custom_trees.act_account_move_bimonthly').read()[0]
        journals=self.env["account.journal"].search([("name","=","Bi Monthly")])
        domain = [('journal_id','in',[i.id for i in journals])]
        action['domain'] = domain
        return action




    @api.onchange('x_student_id_cred',"student_ids")
    def _students_onchange(self):
        self.student_name=''
        self.student_code=" "
        self.campus=""
        self.bill_date=' '
        self.challan_date=' '
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
        self.net_amount=""
        self.std_factsid=""
        self.std_payment_date=""
        self.section_name=""
        self.art=0
        self.biology=0
        self.chemistry=0
        self.physics=0
        self.computing=0
        self.classphoto=0
        self.collegemagazine=0
        self.dc=0
        self.ec=0
        self.farewell=0
        self.gatepass=0
        self.idcard=0
        self.idcardfine=0
        self.latecoming=0
        self.latefee=0
        self.libfine=0
        self.mnf=0
        self.mobfine=0
        self.news=0
        self.paragon=0
        self.books=0
        self.pcopy=0
        self.photo=0
        self.scarf=0
        self.sportd=0
        self.stationary=0
        self.welcome=0
        self.workbook=0
        self.uniform=0
        self.continuation=0
        if self.student_ids:
            full_name=self.student_ids.first_name+" "+self.student_ids.last_name
            self.student_name=full_name
            self.student_code=self.student_ids.facts_udid
            # self.campus=self.student_ids.school_ids.name
            self.challan_date=self.invoice_date
            self.due_date=self.invoice_date_due
            # self.due_amount=self.due_amount
            self.std_name=full_name
            self.std_branch=self.student_ids.school_ids.name
        
            self.std_bill_date=self.invoice_date
            self.std_due_date=self.invoice_date_due
            self.std_discount=self.discount_note
            self.std_reason=self.reject_reason.name
            self.std_batch=self.x_studio_batch.x_name
            self.std_dob=self.student_ids.date_of_birth
            self.std_fathername=self.partner_id.name
            self.std_factsid=self.student_ids.facts_id
            self.std_contactno=self.partner_id.mobile
            self.bill_amount=int(self.amount_total)


            if self.student_ids.tuition_plan_ids:
                tp=self.student_ids.tuition_plan_ids
                for t_plan in tp:
                    if t_plan.journal_id.id==125:
                        self.std_tuition_plan= t_plan.tuition_template_id.name
                    else:
                        self.std_tuition_plan="NO TP"

    
            if self.student_ids.tuition_plan_ids:
                tp=self.student_ids.tuition_plan_ids
                for tp_id in tp:
                    if tp_id.journal_id.id==125:
                        self.std_tuition_plan_state= tp_id.state
                    else:
                        self.std_tuition_plan_state="NO TP"
            
        
            

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
            else:
                if self.grade_level_ids:
                    self.class_name=self.grade_level_ids.name
                else:
                    if self.journal_id.id==119:
                        for nxt_grade in self.student_ids.enrollment_state_ids:
                            self.class_name=nxt_grade.next_grade_level_id.name

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
                        elif 'Admission' in line.product_id.name:
                            adm_amount=int(line.price_subtotal)
                            self.adm_amount=str(adm_amount)
                        elif 'Security' in line.product_id.name:
                           security_amount=int(line.price_subtotal)
                           self.security_amount=str(security_amount)

                        elif 'Class Photo' in line.product_id.name:
                            self.classphoto=line.price_subtotal
                        elif 'College Magazine' in line.product_id.name:
                            self.collegemagazine=line.price_subtotal
                        elif 'Continuation' in line.product_id.name:
                            self.continuation=line.price_subtotal
                        elif 'Discipline' in line.product_id.name:
                            self.dc=line.price_subtotal
                        elif 'Examination' in line.product_id.name:
                            self.ec=line.price_subtotal
                        elif 'Farewell' in line.product_id.name:
                           self.farewell=line.price_subtotal
                        elif 'ID Card Fine' in line.product_id.name:
                            self.idcardfine=line.price_subtotal
                        elif 'Late Coming' in line.product_id.name:
                            self.latecoming=line.price_subtotal
                        elif 'Late Fee' in line.product_id.name:
                            self.latefee=line.price_subtotal
                        elif 'ID Card' in line.product_id.name:
                            self.idcard=line.price_subtotal
                        elif 'Gate Pass' in line.product_id.name:
                            self.gatepass=line.price_subtotal
                        elif 'Miscellaneous & Fine' in line.product_id.name:
                            self.mnf=line.price_subtotal
                        elif 'Mobile Fine' in line.product_id.name:
                           self.mobfine=line.price_subtotal
                        elif 'Newsletter' in line.product_id.name:
                            self.news=line.price_subtotal
                        elif 'Paragon 2nd Child and Onwards' in line.product_id.name:
                            self.paragon=line.price_subtotal
                        elif 'Photocopy (Books)' in line.product_id.name:
                            self.books=line.price_subtotal
                        elif 'Photocopying Charges' in line.product_id.name:
                            self.pcopy=line.price_subtotal
                        elif 'Photograph' in line.product_id.name:
                           self.photo=line.price_subtotal
                        elif 'Scarf' in line.product_id.name:
                            self.scarf=line.price_subtotal
                        elif 'Sports Day' in line.product_id.name:
                            self.sportd=line.price_subtotal
                        elif 'Stationary Charges' in line.product_id.name:
                            self.stationary=line.price_subtotal
                        elif 'Uniform Fine' in line.product_id.name:
                            self.uniform=line.price_subtotal
                        elif 'Wellcome Party' in line.product_id.name:
                           self.welcome=line.price_subtotal
                        elif 'Work Books' in line.product_id.name:
                           self.workbook=line.price_subtotal
                        elif 'Library Fine' in line.product_id.name:
                           self.libfine=line.price_subtotal
                        elif line.product_id.x_studio_code=='ART':
                            self.art=line.price_subtotal
                        elif line.product_id.x_studio_code=='COM':
                            self.computing=line.price_subtotal
                        elif line.product_id.x_studio_code=='CHM':
                            self.chemistry=line.price_subtotal
                        elif line.product_id.x_studio_code=='PHY':
                            self.physics=line.price_subtotal
                        elif line.product_id.x_studio_code=='BIO':
                           self.biology=line.price_subtotal
                      
                        

            
            if self.payment_state=="paid" and self.journal_id==119:
                if self.invoice_payments_widget:
                    var=str(json.loads(self.invoice_payments_widget)["content"][-1]["date"])
                    self.std_payment_date=var
                

            if self.student_ids.school_ids:
                if self.student_ids.enrollment_history_ids:
                    enroll_history=self.student_ids.enrollment_history_ids
                    lst=[]
                    for lines in enroll_history:
                        lst.append(lines.program_id.name)
                    self.campus=lst[0]
            if self.amount_residual:
                self.due_amount=int(self.amount_residual)

            if self.invoice_line_ids: 
                amt=[]
                for line in self.invoice_line_ids:
                    if line.product_id.is_discount_type!=True:
                        amt.append(line.price_total)
                total=sum(amt)
                nofloat=int(total)
                self.net_amount=str(nofloat)
            
               
            
            
                
                        
        

        
               
    



            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            


                        
                    
            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            

