
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
    student_code=fields.Integer(string="UDID")
    student_name=fields.Char(string="Name")
    class_sec=fields.Char(string="Class Section")
    campus=fields.Char(string="Campus")
    bill_date=fields.Date(string="Bill Date")
    due_date=fields.Date(string="Due Date")
    due_amount=fields.Integer(string="Due Amount")

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
    def _onchange_student_data(self):
        monthly_journal=self.env['account.journal'].search([('code','=','MNT')])
        monthly_bill=self.env['account.move'].search([('journal_id','=',monthly_journal.id)])
        for rec in monthly_bill:
            if rec.student_ids:
                full_name=rec.student_ids.first_name+" "+rec.student_ids.last_name
                rec['student_name']=full_name
                rec['student_code']=rec.student_ids.facts_udid
                rec['class_sec']=rec.student_ids.homeroom
                rec['campus']=rec.student_ids.school_ids.name
                rec['bill_date']=rec.invoice_date
                rec['due_date']=rec.invoice_payment_term_id.name
   


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
                        
                    
            
            
            
                




   


                    
   
                    

                    


                    
                

                 
            

