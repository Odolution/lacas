
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
    bill_date=fields.Date(string="Bill Date",compute="_onchange_bill_date_data")
    due_date=fields.Char(string="Due Date",compute="_onchange_due_date_data")
    due_amount=fields.Integer(string="Due Amount",compute="_onchange_due_amount_data")

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
        self.student_code=' '
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
        for rec in monthly_bill:
            if rec.student_ids:
                rec['bill_date']=rec.invoice_date
                
    
    def _get_due_date_field(self):
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
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
                        
                    
            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            

