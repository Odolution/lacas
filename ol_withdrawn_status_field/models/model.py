from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError
import math
from odoo.exceptions import ValidationError
from datetime import datetime

class Account_move(models.Model):
    _inherit= 'account.move' 

    withdrawn_status_reversal_compute = fields.Selection([('Y', 'Y'), ('N', 'N')], compute='_compute_withdrawn_status_reversal',string="Withdrawn Status")
    withdrawn_status_bill_compute = fields.Selection([('Y', 'Y'), ('N', 'N')],compute='_compute_withdrawn_status_bill',string="Withdrawn Status")
    withdrawn_status_reversal = fields.Selection([('Y', 'Y'), ('N', 'N')],string="Withdrawn Status",store = True)
    withdrawn_status_bill = fields.Selection([('Y', 'Y'), ('N', 'N')],string="Withdrawn Status",store = True)




    def _compute_withdrawn_status_reversal(self):
        for rec in self:
            if rec['state']=='posted' and float(rec['amount_residual'])==0:
                rec.withdrawn_status_reversal_compute='Y'
                rec.withdrawn_status_reversal= 'Y'

            else:
                rec.withdrawn_status_reversal_compute='N'
                rec.withdrawn_status_reversal= 'N'


    def _compute_withdrawn_status_bill(self):
        for rec in self:
            if rec['move_type']=='out_invoice' and rec['std_factsid']:
                reversal= self.env['account.move'].search([('move_type','=','out_refund'), ('facts_id_cred_custom','=',rec['std_factsid']),('withdrawn_status_reversal','=','Y'),('state','=','posted')])
                if reversal:
                    rec.withdrawn_status_bill_compute='Y'
                    rec.withdrawn_status_bill= 'Y'
                else:
                    rec.withdrawn_status_bill_compute='N'
                    rec.withdrawn_status_bill= 'N'                    

            else:
                rec.withdrawn_status_bill_compute='N'
                rec.withdrawn_status_bill= 'N'


