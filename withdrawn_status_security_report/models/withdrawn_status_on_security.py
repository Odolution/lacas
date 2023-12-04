from odoo import api,fields,models
from odoo.exceptions import UserError
from datetime import datetime

class WithdrawnStatusOnSecurity(models.Model):
    _inherit=['school.student']

    withdrawn_status_computed=fields.Char(compute='_compute_withdrawn_status_for_security')
    withdrawn_status_security=fields.Char()

    def _compute_withdrawn_status_for_security(self):
        adm_account_move = self.env['account.move'].search([('student_ids', '=', rec.id),('move_type', '=', 'out_invoice'),('journal_id.name', '=', 'Admission Challan')])
        rev_account_move = self.env['account.move'].search([('x_student_id_cred', '=', rec.id),('move_type', '=', 'out_refund'),('journal_id.name', '=', 'Security Deposit')])
            
        for rec in self:
            if adm_account_move:
                rec.withdrawn_status_computed=adm_account_move.withdrawn_status_bill
                rec.withdrawn_status_security=rec.withdrawn_status_computed
            elif rev_account_move:
                rec.withdrawn_status_computed=rev_account_move.withdrawn_status_reversal
                rec.withdrawn_status_security=rec.withdrawn_status_computed
            else:
                rec.withdrawn_status_computed='N/A'
                rec.withdrawn_status_security=rec.withdrawn_status_computed
                

