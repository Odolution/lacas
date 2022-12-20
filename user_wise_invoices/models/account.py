from odoo import models ,fields , api
import json

class UserWiseInvoiceAccount(models.Model):
    _inherit = "account.move"

    # student_id = fields.Integer(string="School")
    
    def get_invoices_action(self):
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        user=self.env["res.users"].search([("id",'=',self.env.uid)])
        domain = [('program_ids','in',[user.user_program_id])]
        action['domain'] = domain
        return action
            
            

