from odoo import api,fields,models
from odoo.exceptions import UserError
from datetime import datetime

class WithdrawnStatusOnSecurity(models.Model):
    _inherit=['school.student']

    withdrawn_status_computed=fields.Char(compute='_compute_withdrawn_status_for_security')
    withdrawn_status_security=fields.Char()
    withdrawn_computed_bool=fields.Boolean()

    def _compute_withdrawn_status_for_security(self):
        withdrawn_computed_bool=False
        adm_account_move = env['account.move'].search([('student_ids', '=', rec.id),('move_type', '=', 'out_invoice'),('journal_id.name', '=', 'Admission Challan')])
        rev_account_move = env['account.move'].search([('x_student_id_cred', '=', rec.id),('move_type', '=', 'out_refund'),('journal_id.name', '=', 'Security Deposit')])
        if adm_account_move:
            for student_record in adm_account_move:
            if student_record['withdrawn_status_bill']:
                self['withdrawn_status_security']=student_record['withdrawn_status_bill']
            else:
                self['withdrawn_status_security']='N/A'
        elif rev_account_move:
            for student_record in rev_account_move:
            if student_record['withdrawn_status_reversal']:
                self['withdrawn_status_security']=student_record['withdrawn_status_reversal']
            else:
                self['withdrawn_status_security']='N/A'
                

