from odoo import models ,fields , api
import json

class UserWiseInvoiceAccount(models.Model):
    _inherit = "account.move"

    # student_id = fields.Integer(string="School")
    
    program_id = fields.Many2one('school.program',string='Program ID')

    @api.onchange('program_ids')
    def calc_program_id(self):
        if self.program_ids: 
            self.program_id = self.program_ids[0]
    
    def get_invoices_action(self):
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        user=self.env["res.users"].search([("id",'=',self.env.uid)])
        domain = [('program_id','in',user.user_program_ids)]
#         domain = []
        action['domain'] = domain
        return action
            
            

