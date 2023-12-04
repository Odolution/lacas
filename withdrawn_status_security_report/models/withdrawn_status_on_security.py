from odoo import api,fields,models
from odoo.exceptions import UserError
from datetime import datetime

class WithdrawnStatusOnSecurity(models.Model):
    _inherit=['school.student']

    withdrawn_status_computed=fields.Char(compute='_compute_withdrawn_status_for_security')
    withdrawn_status_security=fields.Char()

    @api.depends('withdrawn_status_computed')
    def _compute_withdrawn_status_for_security(self):
        account_move = self.env['account.move'].search([('std_factsid', '=', self.facts_id),('journal_id', '=', 'Admission Challan'),
    ('move_type', '=', 'out_invoice')], limit=1)

        if account_move:
            self.withdrawn_status_computed = account_move.withdrawn_status_bill
            self.withdrawn_status_security = account_move.withdrawn_status_bill
        else:
            self.withdrawn_status_security = 'N/A'
            

