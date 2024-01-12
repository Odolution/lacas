
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime



class SecurityCharge(models.Model):

    _inherit = "account.payment"

    def get_security_charge(self):
        for line in self.invoice_line_ids:
            if line.account_id == 2462:
                raise UserError(line.price_unit)