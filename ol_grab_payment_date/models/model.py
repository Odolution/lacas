
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime



class ext_invoice(models.Model):
    _inherit = "account.move"
    ol_payment_date = fields.Date(string='Payment Date')
    @api.onchange('payment_state')
    def onchange_invoice_payments_widget(self):
        print("onchange")
        for rec in self:
            if rec.payment_state == "paid":
                date=""
                try:
                    date=str(json.loads(rec.invoice_payments_widget)["content"][-1]["date"])
                except:
                    pass
                if date!="":
                    rec.ol_payment_date=datetime.datetime.strptime(date,"%Y-%m-%d").date()
                else:
                    rec.ol_payment_date=False
