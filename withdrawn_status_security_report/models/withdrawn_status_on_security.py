from odoo import api,fields,models
from odoo.exceptions import UserError
from datetime import datetime

class WithdrawnStatusOnSecurity(models.Model):
    _inherit=['school.student']

    withdrawn_status_computed=fields.Char()
    withdrawn_status_security=fields.Char()

    def _compute_withdrawn_status_for_security(self):
        pass

