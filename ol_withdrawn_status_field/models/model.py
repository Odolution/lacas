from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError
import math
from odoo.exceptions import ValidationError
from datetime import datetime

class account(models.Model):
    _inherit= 'account.move'

    withdrawn_status = fields.Selection([('Y', 'Y'), ('N', 'N')],string="Withdrawn Status", compute='_compute_withdrawn_status')


    # @api.depends('state','amount_residual')
    def _compute_withdrawn_status(self):
        for rec in self:
            if rec['state']=='posted' and float(rec['amount_residual'])==0:
                rec.withdrawn_status= 'Y'

            else:
                rec.withdrawn_status= 'N'


