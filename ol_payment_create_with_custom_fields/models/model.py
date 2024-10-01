
from odoo import models, api, fields, _
from odoo.exceptions import UserError




class extwiz(models.TransientModel):
    _inherit = "account.payment.register"
    ol_check_in_favor_of = fields.Char('Check in Favor Of')
    
    @api.model
    def _create_payments(self):
        payments=super(extwiz,self)._create_payments()

        for payment in payments:
            payment.ol_check_in_favor_of = self.ol_check_in_favor_of
        return payments
class extpayment(models.Model):
    _inherit = "account.payment"
    ol_check_in_favor_of = fields.Char('Check in Favor Of')
