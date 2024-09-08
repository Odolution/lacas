
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
import json
from datetime import datetime

class ext(models.Model):
    _inherit="account.move"
    udid_bill = fields.Char(string='UDID Bills', related='student_ids_ol_new.olf_udid') # Yaminah
    # udid_bill = fields.Char(string='UDID Bills',)
    student_ids_ol_new = fields.Many2one('school.student', string="std ol new",compute='get_student',store=True) # Yaminah
    
    student_ids_ol=fields.Many2one('school.student', string="std ol") # compute='_feild_students' removed from here
    x_studio_udid_monthly_bills = fields.Char(string="UDID Bills",related='student_ids_ol.name')
    x_studio_olf_id_bills = fields.Integer(string="OLF ID Bills",related='student_ids_ol.olf_id')
    x_studio_olf = fields.Integer(string="OLF",related='student_ids_ol.olf_id')
    #student_ids_ol=fields.Many2one('school.student', string="std ol")
    tuition=fields.Integer(string="Tuition Fee")
    club=fields.Integer(string="Club Charges")
    computer=fields.Integer(string="computer Charges")
    library=fields.Integer(string="library Charges")
    utility=fields.Integer(string="Utility AC/Generator")
    student_code=fields.Char(string="UDID", compute="_compute_UDID")
    #student_code=fields.Char(string="UDID")
    student_name=fields.Char(string="Name",related='student_ids_ol_new.name')
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
    std_current_branch=fields.Char(string="Current Branch", related='student_ids_ol_new.x_last_school_id.name')
    std_dob=fields.Date(string="Date of Birth", related='student_ids_ol_new.date_of_birth')
    std_name=fields.Char(string="Student",related='student_ids_ol_new.name')
    std_batch=fields.Char(string="Batch", related='student_ids_ol_new.x_studio_batchsession')
    std_discount=fields.Char(string="Discount note empty ")
    std_reason=fields.Char(string="Concession Name empty")
    std_fathername=fields.Char(string="Father Name", compute='_compute_father_name')
    #std_fathername=fields.Char(string="Father Name")
    std_contactno=fields.Char(string="Contact No.", related='student_ids_ol_new.mobile')
    adm_amount=fields.Char(string="Admission Amount")
    security_amount=fields.Char(string="Security Amount")
    bill_amount=fields.Char(string="Bill Amount")
    net_amount=fields.Char(string="Net Amount",compute="_compute_net_amnt")
    std_olfid2=fields.Char(string="olf ID",compute="_compute_olf_id")
    std_olfid=fields.Char(string="olf ID")
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
    latefee=fields.Integer(string="Late Fee", compute="_compute_late_fee_amnt")
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
    Holiday_homework=fields.Integer(string="Holiday Homework")
    Technology_Charges= fields.Integer(string="Technology Charges")
    orb=fields.Integer(string="Orb")


    # Added by Anas Bin Ateeq
    oxford=fields.Integer(string="Oxford E Mate Charges")
    utility_charges=fields.Integer(string="Utility Charges")
    #########################################################
#maaz
    def js_assign_outstanding_line_custom(invoice,line_id):
        invoice.sudo().js_assign_outstanding_line(line_id)
        return True

#maaz

    def get_student(self):
        for rec_std in self:
            if rec_std.student_ids:
                rec_std.student_ids_ol_new=rec_std.student_ids.id
            else:
                rec_std.student_ids_ol_new=False

    def _feild_students(self):
        for rec_std in self:
            if rec_std.student_ids:
                rec_std.student_ids_ol=rec_std.student_ids.id
            else:
                rec_std.student_ids_ol=''


    def _compute_UDID(self):

        self.student_code=""
        for rec in self:
            if rec.student_ids:
                    rec.student_code=rec.student_ids.olf_udid

    def _compute_olf_id(self):
        self.std_olfid2=""
        for rec_id in self:
            if rec_id.student_ids:
                rec_id.std_olfid2=rec_id.student_ids.olf_id
                rec_id.std_olfid=rec_id.student_ids.olf_id


    def _compute_father_name(self):
        for rec in self:
            rec.std_fathername=rec.partner_id.name
            # for relation in rec.student_ids.relationship_ids:
            #     if relation.relationship_type_id.name == "Father":
            #         rec.std_fathername = relation.individual_id.name
            #     else:
            #         rec.std_fathername = ""

                

    # def _compute_net_amnt(self):
    #     for rec in self:
    #         if rec.invoice_line_ids:
    #             amt=[]
    #             for line in rec.invoice_line_ids:
    #                 # if line.product_id.name!="Late Fee":
    #                 #     amt.append(line.price_total)
    #                 if line.product_id.is_discount_type!=True:
    #                     #if line.product_id.name!="Late Fee":
    #                     amt.append(line.price_total)
    #             total=sum(amt)
    #             nofloat=int(total)
    #             rec.net_amount=str(nofloat)

    def _compute_late_fee_amnt(self):
        self.latefee=0
        for rec in self:
            if rec.invoice_line_ids:

                for line in rec.invoice_line_ids:
                    if line.product_id:
                        if line.product_id.name and 'Late Fee' in line.product_id.name:
                            rec.latefee=line.price_total
                    # else:
                    #     rec.latefee=0

    def _compute_net_amnt(self):
        for rec in self:
            if rec.invoice_line_ids:
                amt=[]
                late=[]
                concession=[]
                for line in rec.invoice_line_ids:
                    # if line.product_id.name!="Late Fee":
                    #     amt.append(line.price_total)
                    if line.product_id.is_discount_type!=True:
                        #if line.product_id.name!="Late Fee":
                        amt.append(line.price_total)
                    if line.product_id.name and 'Late Fee' in line.product_id.name:
                        late.append(line.price_total)
                    else:
                        late.append(0)

                    if line.product_id.is_discount_type==True:
                        #if line.product_id.name!="Late Fee":
                        abs_price=abs(line.price_total)
                        concession.append(abs_price)


                #if amt:
                total=sum(amt)
                total_consession=sum(concession)
                late_deduct_tot=sum(late)

                if late_deduct_tot>0:
                    amnt_after=abs(total-late_deduct_tot-total_consession)
                    rec.net_amount=str(amnt_after)
                #raise UserError(amnt_after)
                else:
                    amnt_total_wo_latefee=abs(total-total_consession)
                    #nofloat=int(total)
                    #raise UserError(amnt_total_wo_latefee)

                    rec.net_amount=str(amnt_total_wo_latefee)
                #nofloat_tot=int(amnt_after)
            else:
                 rec.net_amount="0"






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


    @api.onchange('invoice_line_ids')
    def _invoice_lines_onchange(self):
        for rec_inv in self:

            if rec_inv.invoice_line_ids: 

                rec_inv.tuition=0
                rec_inv.club=0
                rec_inv.computer=0
                rec_inv.library=0
                rec_inv.utility=0
                rec_inv.art=0
                rec_inv.biology=0
                rec_inv.chemistry=0
                rec_inv.physics=0
                rec_inv.computing=0
                rec_inv.classphoto=0
                rec_inv.collegemagazine=0
                rec_inv.dc=0
                rec_inv.ec=0
                rec_inv.farewell=0
                rec_inv.gatepass=0
                rec_inv.idcard=0
                rec_inv.idcardfine=0
                rec_inv.latecoming=0
                rec_inv.latefee=0
                rec_inv.libfine=0
                rec_inv.mnf=0
                rec_inv.mobfine=0
                rec_inv.news=0
                rec_inv.paragon=0
                rec_inv.books=0
                rec_inv.pcopy=0
                rec_inv.photo=0
                rec_inv.scarf=0
                rec_inv.sportd=0
                rec_inv.stationary=0
                rec_inv.welcome=0
                rec_inv.workbook=0
                rec_inv.uniform=0
                rec_inv.continuation=0
                rec_inv.adm_amount=""
                rec_inv.Holiday_homework=0
                rec_inv.Technology_Charges=0
                rec_inv.utility_charges=0
                rec_inv.oxford=0
                rec_inv.orb=0



                for line in rec_inv.invoice_line_ids:
                    if 'Tuition Fee' in line.product_id.name:
                        rec_inv.tuition=line.price_subtotal
                    elif 'Club' in line.product_id.name:
                        rec_inv.club=line.price_subtotal
                    elif 'Computer' in line.product_id.name:
                        rec_inv.computer=line.price_subtotal
                    elif 'Library' in line.product_id.name:
                        rec_inv.library=line.price_subtotal
                    elif 'AC/Generator' in line.product_id.name:
                        rec_inv.utility=line.price_subtotal
                    elif 'Utility' in line.product_id.name:
                        rec_inv.utility_charges=line.price_subtotal
                    elif 'OXFORD' in line.product_id.name:
                        rec_inv.oxford=line.price_subtotal

                    elif 'Admission' in line.product_id.name and not line.product_id.is_discount_type:
                        adm_amount_charge=int(line.price_subtotal)
                        rec_inv.adm_amount=str(adm_amount_charge)

                    elif 'Admission' in line.product_id.name and line.product_id.is_discount_type:
                        disc_adm_amount=int(line.price_subtotal)
                        calculated_adm=adm_amount_charge+disc_adm_amount
                        rec_inv.adm_amount=str(calculated_adm)
                        



                    elif 'Security' in line.product_id.name and not line.product_id.is_discount_type:
                        security_amount_charge=int(line.price_subtotal)
                        rec_inv.security_amount=str(security_amount_charge)


                    elif 'Security' in line.product_id.name and line.product_id.is_discount_type:
                        discount_security=int(line.price_subtotal)
                        calculated_security=security_amount_charge+discount_security
                        rec_inv.security_amount=str(calculated_security)

                    elif 'Class Photo' in line.product_id.name:
                        rec_inv.classphoto=line.price_subtotal
                    elif 'College Magazine' in line.product_id.name:
                        rec_inv.collegemagazine=line.price_subtotal
                    elif 'Continuation' in line.product_id.name:
                        rec_inv.continuation=line.price_subtotal
                    elif 'Discipline' in line.product_id.name:
                        rec_inv.dc=line.price_subtotal
                    elif 'Examination' in line.product_id.name:
                        rec_inv.ec=line.price_subtotal
                    elif 'Farewell' in line.product_id.name:
                        rec_inv.farewell=line.price_subtotal
                    elif 'ID Card Fine' in line.product_id.name:
                        rec_inv.idcardfine=line.price_subtotal
                    elif 'Late Coming' in line.product_id.name:
                        rec_inv.latecoming=line.price_subtotal
                    elif line.product_id.name and  'Late Fee' in line.product_id.name:
                        rec_inv.latefee=line.price_subtotal
                    elif 'ID Card' in line.product_id.name:
                        rec_inv.idcard=line.price_subtotal
                    elif 'Gate Pass' in line.product_id.name:
                        rec_inv.gatepass=line.price_subtotal
                    elif 'Miscellaneous & Fine' in line.product_id.name:
                        rec_inv.mnf=line.price_subtotal
                    elif 'Mobile Fine' in line.product_id.name:
                        rec_inv.mobfine=line.price_subtotal
                    elif 'Newsletter' in line.product_id.name:
                        rec_inv.news=line.price_subtotal
                    elif 'Paragon 2nd Child and Onwards' in line.product_id.name:
                        rec_inv.paragon=line.price_subtotal
                    elif 'Photocopy (Books)' in line.product_id.name:
                        rec_inv.books=line.price_subtotal
                    elif 'Photocopying Charges' in line.product_id.name:
                        rec_inv.pcopy=line.price_subtotal
                    elif 'Photograph' in line.product_id.name:
                        rec_inv.photo=line.price_subtotal
                    elif 'Scarf' in line.product_id.name:
                        rec_inv.scarf=line.price_subtotal
                    elif 'Sports Day' in line.product_id.name:
                        rec_inv.sportd=line.price_subtotal
                    elif 'Stationary Charges' in line.product_id.name:
                        rec_inv.stationary=line.price_subtotal
                    elif 'Uniform Fine' in line.product_id.name:
                        rec_inv.uniform=line.price_subtotal
                    elif 'Welcome Party' in line.product_id.name:
                        rec_inv.welcome=line.price_subtotal
                    elif 'Work Books' in line.product_id.name:
                        rec_inv.workbook=line.price_subtotal
                    elif 'Library Fine' in line.product_id.name:
                        rec_inv.libfine=line.price_subtotal
                    elif 'Holiday Homework' in line.product_id.name:
                        rec_inv.Holiday_homework=line.price_subtotal
                    elif 'Technology Charge' in line.product_id.name:
                        rec_inv.Technology_Charges=line.price_subtotal
                    elif 'ORB' in line.product_id.name:
                        rec_inv.orb=line.price_subtotal
                    elif line.product_id.x_studio_code=='ART':
                        rec_inv.art=line.price_subtotal
                    elif line.product_id.x_studio_code=='COM':
                        rec_inv.computing=line.price_subtotal
                    elif line.product_id.x_studio_code=='CHM':
                        rec_inv.chemistry=line.price_subtotal
                    elif line.product_id.x_studio_code=='PHY':
                        rec_inv.physics=line.price_subtotal
                    elif line.product_id.x_studio_code=='BIO':
                        rec_inv.biology=line.price_subtotal
                
            wholename=""
            if rec_inv.student_ids.homeroom:
                wholename=rec_inv.student_ids.homeroom
                splitted_name=wholename.split('-')
                if len(splitted_name)>2:
                    #self.class_name=splitted_name[0]+"-"+splitted_name[1]
                    rec_inv.class_name=rec_inv.grade_level_ids.name
                    rec_inv.section_name=splitted_name[2]
                elif len(splitted_name)>1:
                    #self.class_name=splitted_name[0]
                    rec_inv.class_name=rec_inv.grade_level_ids.name
                    rec_inv.section_name=splitted_name[1]
                elif len(splitted_name)>0:
                    
                    rec_inv.class_name=rec_inv.grade_level_ids.name
                        #self.class_name=splitted_name[0]
            else:
                if rec_inv.grade_level_ids:
                    rec_inv.class_name=rec_inv.grade_level_ids.name
                else:
                    if rec_inv.journal_id.id==119:
                        for nxt_grade in rec_inv.student_ids.enrollment_state_ids:
                            rec_inv.class_name=nxt_grade.next_grade_level_id.name

            wholedate=str(rec_inv.invoice_date)
            splitted_name=wholedate.split('-')
            if rec_inv.journal_id.id==125 or rec_inv.journal_id.id == 119:
                if len(splitted_name)>2:
                    month=splitted_name[1]
                    wholeyear=splitted_name[0]
                    year=wholeyear[2:4]
                    if month =='01':
                        rec_inv.bill_date="Jan"+"-"+year
                    elif month =='02':
                        rec_inv.bill_date="Feb"+"-"+year
                    elif month =='03':
                        rec_inv.bill_date="Mar"+"-"+year
                    elif month =='04':
                        rec_inv.bill_date="Apr"+"-"+year
                    elif month =='05':
                        rec_inv.bill_date="May"+"-"+year
                    elif month =='06':
                        rec_inv.bill_date="Jun"+"-"+year
                    elif month =='07':
                        rec_inv.bill_date="Jul"+"-"+year
                    elif month =='08':
                        rec_inv.bill_date="Aug"+"-"+year
                    elif month =='09':
                        rec_inv.bill_date="Sep"+"-"+year
                    elif month =='10':
                        rec_inv.bill_date="Oct"+"-"+year
                    elif month =='11':
                        rec_inv.bill_date="Nov"+"-"+year
                    elif month =='12':
                        rec_inv.bill_date="Dec"+"-"+year
            
            if rec_inv.journal_id.id==126:
                rec_inv.bill_date=rec_inv.bi_monthly_cycle+"-"+rec_inv.invoice_date.strftime('%y')

            # Yaminah
            if rec_inv.journal_id.id==119:
                if rec_inv.invoice_date:
                    date_obj = datetime.strptime(str(rec_inv.invoice_date), '%Y-%m-%d')
                    rec_inv.bill_date = date_obj.strftime('%B-%y').capitalize()
            # Yaminah

    @api.onchange('x_student_id_cred',"student_ids")
    def _students_onchange(self):
        #self.student_name=''
        #self.student_code=" "
        #self.campus=""
        self.bill_date=' '
        # self.challan_date=' '
        # self.due_date=' '
        # self.due_amount=0
        
        self.class_name=""
        # self.std_bill_date=""
        # self.std_due_date=""
        self.std_branch=' '
        #self.std_current_branch=''
        #self.std_dob=' '
        self.std_name=""
        #self.std_batch=""
        #self.std_discount=""
        #self.std_reason=""
        #self.std_fathername=""
        #self.std_contactno=""
        
        self.security_amount=""
        self.bill_amount=""
        #self.net_amount=""
        #self.std_olfid=""
        self.std_payment_date=""
        self.section_name=""
       
        if self.student_ids:
            full_name=self.student_ids.first_name+" "+self.student_ids.last_name
            #self.student_name=full_name
            #self.student_code=self.student_ids.olf_udid
            # self.campus=self.student_ids.school_ids.name
            # self.challan_date=self.invoice_date
            # self.due_date=self.invoice_date_due
            # self.due_amount=self.due_amount
            # self.std_name=full_name
            # if len(self.student_ids.school_ids) > 1:
            #     #self.std_current_branch=self.student_ids.x_last_school_id.name
            #     for sch in self.student_ids.school_ids:
            #         if sch==1:
            #             self.std_branch=self.student_ids.school_ids.name
            # else:
            #     self.std_branch=self.student_ids.school_ids.name
                #self.std_current_branch=self.student_ids.school_ids.name
                # for sch in self.student_ids.school_ids:
                #     if sch==1:
                        
        
            self.std_bill_date=self.invoice_date
            # self.std_due_date=self.invoice_date_due
            #self.std_discount=self.discount_note
            #self.std_reason=self.reject_reason.name
            #self.std_batch=self.x_studio_batch.x_name
            #self.std_dob=self.student_ids.date_of_birth
            #self.std_fathername=self.partner_id.name
           # self.std_olfid=self.student_ids.olf_id
            #self.std_contactno=self.partner_id.mobile
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
                    #self.class_name=splitted_name[0]+"-"+splitted_name[1]
                    self.class_name=self.grade_level_ids.name
                    self.section_name=splitted_name[2]
                elif len(splitted_name)>1:
                    #self.class_name=splitted_name[0]
                    self.class_name=self.grade_level_ids.name
                    self.section_name=splitted_name[1]
                elif len(splitted_name)>0:
                    
                    self.class_name=self.grade_level_ids.name
                        #self.class_name=splitted_name[0]
            else:
                if self.grade_level_ids:
                    self.class_name=self.grade_level_ids.name
                else:
                    if self.journal_id.id==119:
                        for nxt_grade in self.student_ids.enrollment_state_ids:
                            self.class_name=nxt_grade.next_grade_level_id.name

            wholedate=str(self.invoice_date)
            splitted_name=wholedate.split('-')
            if self.journal_id.id==125 :
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
            
            if self.journal_id.id==126:
                self.bill_date=self.bi_monthly_cycle+"-"+self.invoice_date.strftime('%y')

            # Yaminah
            if self.journal_id.id==119:
                if self.invoice_date:
                    date_obj = datetime.strptime(str(self.invoice_date), '%Y-%m-%d')
                    self.bill_date = date_obj.strftime('%B-%y').capitalize()
            # Yaminah    
    
            # if self.invoice_line_ids: 
            #         for line in self.invoice_line_ids:
            #             if 'Tuition Fee' in line.product_id.name:
            #                  self.tuition=line.price_subtotal
            #             elif 'Club' in line.product_id.name:
            #                 self.club=line.price_subtotal
            #             elif 'Computer' in line.product_id.name:
            #                 self.computer=line.price_subtotal
            #             elif 'Library' in line.product_id.name:
            #                 self.library=line.price_subtotal
            #             elif 'Utility' in line.product_id.name:
            #                 self.utility=line.price_subtotal
            #             elif 'Admission' in line.product_id.name:
            #                 adm_amount=int(line.price_subtotal)
            #                 self.adm_amount=str(adm_amount)
            #             elif 'Security' in line.product_id.name:
            #                security_amount=int(line.price_subtotal)
            #                self.security_amount=str(security_amount)

            #             elif 'Class Photo' in line.product_id.name:
            #                 self.classphoto=line.price_subtotal
            #             elif 'College Magazine' in line.product_id.name:
            #                 self.collegemagazine=line.price_subtotal
            #             elif 'Continuation' in line.product_id.name:
            #                 self.continuation=line.price_subtotal
            #             elif 'Discipline' in line.product_id.name:
            #                 self.dc=line.price_subtotal
            #             elif 'Examination' in line.product_id.name:
            #                 self.ec=line.price_subtotal
            #             elif 'Farewell' in line.product_id.name:
            #                self.farewell=line.price_subtotal
            #             elif 'ID Card Fine' in line.product_id.name:
            #                 self.idcardfine=line.price_subtotal
            #             elif 'Late Coming' in line.product_id.name:
            #                 self.latecoming=line.price_subtotal
            #             elif 'Late Fee' in line.product_id.name:
            #                 self.latefee=line.price_subtotal
            #             elif 'ID Card' in line.product_id.name:
            #                 self.idcard=line.price_subtotal
            #             elif 'Gate Pass' in line.product_id.name:
            #                 self.gatepass=line.price_subtotal
            #             elif 'Miscellaneous & Fine' in line.product_id.name:
            #                 self.mnf=line.price_subtotal
            #             elif 'Mobile Fine' in line.product_id.name:
            #                self.mobfine=line.price_subtotal
            #             elif 'Newsletter' in line.product_id.name:
            #                 self.news=line.price_subtotal
            #             elif 'Paragon 2nd Child and Onwards' in line.product_id.name:
            #                 self.paragon=line.price_subtotal
            #             elif 'Photocopy (Books)' in line.product_id.name:
            #                 self.books=line.price_subtotal
            #             elif 'Photocopying Charges' in line.product_id.name:
            #                 self.pcopy=line.price_subtotal
            #             elif 'Photograph' in line.product_id.name:
            #                self.photo=line.price_subtotal
            #             elif 'Scarf' in line.product_id.name:
            #                 self.scarf=line.price_subtotal
            #             elif 'Sports Day' in line.product_id.name:
            #                 self.sportd=line.price_subtotal
            #             elif 'Stationary Charges' in line.product_id.name:
            #                 self.stationary=line.price_subtotal
            #             elif 'Uniform Fine' in line.product_id.name:
            #                 self.uniform=line.price_subtotal
            #             elif 'Wellcome Party' in line.product_id.name:
            #                self.welcome=line.price_subtotal
            #             elif 'Work Books' in line.product_id.name:
            #                self.workbook=line.price_subtotal
            #             elif 'Library Fine' in line.product_id.name:
            #                self.libfine=line.price_subtotal
            #             elif line.product_id.x_studio_code=='ART':
            #                 self.art=line.price_subtotal
            #             elif line.product_id.x_studio_code=='COM':
            #                 self.computing=line.price_subtotal
            #             elif line.product_id.x_studio_code=='CHM':
            #                 self.chemistry=line.price_subtotal
            #             elif line.product_id.x_studio_code=='PHY':
            #                 self.physics=line.price_subtotal
            #             elif line.product_id.x_studio_code=='BIO':
            #                self.biology=line.price_subtotal
                      
                        

            
            if self.payment_state=="paid" and self.journal_id==119:
                if self.invoice_payments_widget:
                    var=str(json.loads(self.invoice_payments_widget)["content"][-1]["date"])
                    self.std_payment_date=var
                

            # if self.student_ids.school_ids:
            #     if self.student_ids.enrollment_history_ids:
            #         enroll_history=self.student_ids.enrollment_history_ids
            #         lst=[]
            #         for lines in enroll_history:
            #             lst.append(lines.program_id.name)
            #         self.campus=lst[0]
            if self.amount_residual:
                self.due_amount=int(self.amount_residual)

            # if self.invoice_line_ids: 
            #     amt=[]
            #     for line in self.invoice_line_ids:
            #         if line.product_id.is_discount_type!=True:
            #             amt.append(line.price_total)
            #     total=sum(amt)
            #     nofloat=int(total)
            #     self.net_amount=str(nofloat)
            
               
            
            
                
                        
        

        
               
    



            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            


                        
                    
            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            

