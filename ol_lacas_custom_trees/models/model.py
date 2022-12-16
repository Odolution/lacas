
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class ext(models.Model):
    _inherit="account.move"
    # security_price=fields.Integer(string='Security Price')
   
    tuition=fields.Integer(string="Tuition Fee", compute='_onchange_tuition')
    club=fields.Integer(string="Club Charges", compute="_onchange_club")
    computer=fields.Integer(string="computer Charges", compute="_onchange_computer")
    library=fields.Integer(string="library Charges", compute="_onchange_library")
    utility=fields.Integer(string="utility Charges", compute="_onchange_utility")
    student_code=fields.Integer(string="Student Code",compute="_onchange_student_code_data")
    student_name=fields.Char(string="Name",compute="_onchange_student_name_data")
    class_sec=fields.Char(string="Class Section",compute="_onchange_class_sec_data")
    campus=fields.Char(string="Campus",compute="_onchange_campus_data")
    bill_date=fields.Char(string="Bill Date",compute="_onchange_bill_date_data")
    due_date=fields.Char(string="Due Date",compute="_onchange_due_date_data")
    due_amount=fields.Integer(string="Due Amount",compute="_onchange_due_amount_data")
    
    
    std_udid=fields.Integer(string="UDID",compute="_onchange_udid_data")
    std_class=fields.Char(string="Class",compute="_onchange_class_data")
    std_bill_date=fields.Char(string="Issue Date",compute="_onchange_std_bill_date_data")
    std_due_date=fields.Char(string="Due Date",compute="_onchange_std_due_date_data")
    std_branch=fields.Char(string="Branch",compute="_onchange_branch_data")
    std_dob=fields.Char(string="Date of Birth",compute="_onchange_dob_data")
    std_name=fields.Char(string="Student",compute="_onchange_std_name_data")
    std_batch=fields.Char(string="Batch",compute="_onchange_batch_data")
    std_discount=fields.Char(string="Discount note",compute="_onchange_std_discount_data")
    std_reason=fields.Char(string="Concession Name",compute="_onchange_std_reason_data")
    std_fathername=fields.Char(string="Father Name",compute="_onchange_std_fathername_data")
    std_contactno=fields.Char(string="Contact No.",compute="_onchange_std_contactno_data")
    adm_amount=fields.Char(string="Admission Amount",compute="_onchange_adm_amount_data")

    

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
    
    def get_securityDeposit_action(self):
        action = self.env.ref('ol_lacas_custom_trees.act_account_move_securityDeposit').read()[0]
        journals=self.env["account.journal"].search([("name","=","Security Deposit")])
        domain = [('journal_id','in',[i.id for i in journals])]
        action['domain'] = domain
        return action  

    
    @api.onchange('invoice_line_ids')
    def _onchange_tuition(self):
        self._get_price_field()

    @api.onchange('invoice_line_ids')
    def _onchange_club(self):
        self._get_club_field()

    @api.onchange('invoice_line_ids')
    def _onchange_computer(self):
        self._get_computer_field()

    @api.onchange('invoice_line_ids')
    def _onchange_library(self):
        self._get_library_field()

    @api.onchange('invoice_line_ids')
    def _onchange_utility(self):
        self._get_utility_field()

    @api.onchange('student_ids')
    def _onchange_student_name_data(self):
        self._get_student_name_field()
    
    @api.onchange('student_ids')
    def _onchange_student_code_data(self):
        self._get_student_code_field()
    
    @api.onchange('student_ids')
    def _onchange_class_sec_data(self):
        self._get_class_sec_field()

    @api.onchange('student_ids')
    def _onchange_campus_data(self):
        self._get_campus_field()
    
    
    @api.onchange('student_ids')
    def _onchange_bill_date_data(self):
        self._get_bill_date_field()

    @api.onchange('student_ids')
    def _onchange_due_date_data(self):
        self._get_due_date_field()
        
    @api.onchange('student_ids')
    def _onchange_due_amount_data(self):
        self._get_due_amount_field()
        

       
    
    

    
        
       

    def _get_student_name_field(self):
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
        self.student_name=' '
        for rec in monthly_bill:
            if rec.student_ids:
                full_name=rec.student_ids.first_name+" "+rec.student_ids.last_name
                rec['student_name']=full_name


    def _get_student_code_field(self):
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
        self.student_code=0
        for rec in monthly_bill:
            if rec.student_ids:
                rec['student_code']=rec.student_ids.facts_udid
    
    def _get_class_sec_field(self):
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
        self.class_sec=' '
        for rec in monthly_bill:
            if rec.student_ids:
                rec['class_sec']=rec.student_ids.homeroom

    def _get_campus_field(self):
        
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
        self.campus=' '
        for rec in monthly_bill:
            if rec.student_ids:
                rec['campus']=rec.student_ids.school_ids.name
                

    def _get_bill_date_field(self):
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
        self.bill_date=' '
        for rec in monthly_bill:
            if rec.student_ids:
                rec['bill_date']=rec.invoice_date
                
    
    def _get_due_date_field(self):
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
        self.due_date=' '
        for rec in monthly_bill:
            if rec.student_ids:
                rec['due_date']=rec.invoice_date_due
               
    def _get_due_amount_field(self):
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
        self.due_amount=0
        for rec in monthly_bill:
            if rec.student_ids:
                rec['due_amount']=rec.due_amount


    def _get_price_field(self):
        monthly_bill=self.env['account.move'].search([('journal_id','=',125)])
        self.tuition=0
        for rec in monthly_bill:
                if rec.invoice_line_ids: 
                    for line in rec.invoice_line_ids:
                        if 'Tuition Fee' in line.product_id.name:
                            rec['tuition']=line.price_subtotal
                        

    def _get_club_field(self):
        monthly_bill=self.env['account.move'].search([('journal_id','=',125)])
        self.club=0
        for rec in monthly_bill:
                if rec.invoice_line_ids: 
                    for line in rec.invoice_line_ids:
                        if 'Club' in line.product_id.name:
                            rec['club']=line.price_subtotal
                        

    def _get_computer_field(self):
        monthly_bill=self.env['account.move'].search([('journal_id','=',125)])
        self.computer=0
        for rec in monthly_bill:
                if rec.invoice_line_ids: 
                    for line in rec.invoice_line_ids:
                        if 'Computer' in line.product_id.name:
                            rec['computer']=line.price_subtotal
                       

    def _get_library_field(self):

        monthly_bill=self.env['account.move'].search([('journal_id','=',125)])
        self.library=0
        for rec in monthly_bill:
                if rec.invoice_line_ids: 
                    for line in rec.invoice_line_ids:
                        if 'Library' in line.product_id.name:
                            rec['library']=line.price_subtotal
                
    def _get_utility_field(self):
        monthly_bill=self.env['account.move'].search([('journal_id','=',125)])
        self.utility=0
        for rec in monthly_bill:
                if rec.invoice_line_ids: 
                    for line in rec.invoice_line_ids:
                        if 'Utility' in line.product_id.name:
                            rec['utility']=line.price_subtotal
                            
  #admission


    
    @api.onchange('student_ids')
    def _onchange_std_name_data(self):
        self._get_std_name_field()

    def _get_std_name_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_name=''
        
        for rec in adm_journals:
            
            if rec.student_ids:
                full_name=rec.student_ids.first_name+" "+rec.student_ids.last_name
                rec['std_name']=full_name

    
    @api.onchange('student_ids')
    def _onchange_dob_data(self):
        self._get_dob_field()
    
                
    def _get_dob_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_dob=' '
        for rec in adm_journals:

            rec.std_dob=' '
            if rec.student_ids:
                rec['std_dob']=rec.student_ids.date_of_birth
    


    
    @api.onchange('student_ids')
    def _onchange_udid_data(self):
        self._get_udid_field()
    
                
    def _get_udid_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_udid=0
        for rec in adm_journals:

           
            if rec.student_ids:
                rec['std_udid']=rec.student_ids.facts_udid

    @api.onchange('student_ids')
    def _onchange_adm_amount_data(self):
        self._get_adm_amt_field()
    
                
    def _get_adm_amt_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.adm_amount=0
        for rec in adm_journals:

           
            if rec.student_ids:
                rec['adm_amount']=rec.tax_totals_json[16:24]



    @api.onchange('student_ids')
    def _onchange_std_discount_data(self):
        self._get_std_discount_field()
    
                
    def _get_std_discount_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_discount=''
        for rec in adm_journals:
            if rec.student_ids:
                rec['std_discount']=rec.discount_note
    
    @api.onchange('student_ids')
    def _onchange_std_reason_data(self):
        self._get_std_reason_field()
    
                
    def _get_std_reason_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_reason=''
        for rec in adm_journals:
            if rec.student_ids:
                rec['std_reason']=rec.reject_reason
    
    

    @api.onchange('student_ids')
    def _onchange_batch_data(self):
        self._get_batch_field()
    
                
    def _get_batch_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_batch=''
        for rec in adm_journals:
            if rec.student_ids:
                rec['std_batch']=rec.x_studio_batch
    
    
    @api.onchange('student_ids')
    def _onchange_class_data(self):
        self._get_class_field()

    
    def _get_class_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_class=' '
        for rec in adm_journals:
            if rec.student_ids:

                rec['std_class']=rec.student_ids.homeroom
   
    @api.onchange('student_ids')
    def _onchange_std_fathername_data(self):
        self._get_father_field()

    
    def _get_father_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_fathername=' '
        for rec in adm_journals:
            if rec.student_ids:

                rec['std_fathername']=rec.partner_id.name

    @api.onchange('student_ids')
    def _onchange_std_contactno_data(self):
        self._get_contactno_field()

    
    def _get_contactno_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_contactno=' '
        for rec in adm_journals:
            if rec.student_ids:
                rec['std_contactno']=rec.partner_id.mobile


    
    
    @api.onchange('student_ids')
    def _onchange_branch_data(self):
        self._get_branch_field()

    def _get_branch_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_branch=' '
        for rec in adm_journals:
            if rec.student_ids:
                rec['std_branch']=rec.student_ids.school_ids.name
                
    
    
    @api.onchange('student_ids')
    def _onchange_std_bill_date_data(self):
        self._get_std_bill_date_field()

    def _get_std_bill_date_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_bill_date=' '
        for rec in adm_journals:
            if rec.student_ids:
                rec['std_bill_date']=rec.invoice_date

    @api.onchange('student_ids')
    def _onchange_std_due_date_data(self):
        self._get_std_due_date_field()

    def _get_std_due_date_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.std_due_date=' '
        for rec in adm_journals:
            if rec.student_ids:
                rec['std_due_date']=rec.invoice_date_due  
   
            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            


                        
                    
            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            

