
from odoo import models, api, fields, _
from odoo.exceptions import UserError





class ext_invoice(models.Model):
    _inherit = "account.move"
    ol_payment_date = fields.Char(string='Payment Date')
    @api.onchange('invoice_payments_widget')
    def onchange_invoice_payments_widget(self):
        for rec in self:
            if rec.invoice_payments_widget:
                raise UserError(rec.invoice_payments_widget)
    
