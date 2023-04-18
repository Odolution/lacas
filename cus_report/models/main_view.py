# import datetime
# from re import U

from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import http
from odoo.http import request
from datetime import datetime 
# import base64
# import requests
# import datetime

# class OLStartDate(models.Model):
#     _inherit = 'contract.order'

#     def change_start_date(self,context):
#         active_ids = self.env.context.get('active_ids')
#         return {
#             'name': _('Change Order Start Date'),
#             'view_mode': 'form',
#             'res_model': 'contract.order.change.start.date',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'context': {
#                 'contract_id': self.id,
#             },
#             'target': 'new'
#         }


class inheritincompany(models.Model):
    _inherit = 'res.company'

    image = fields.Image(string='Bank Image')
    
class reportbutton(http.Controller):
    @http.route('/attachment/download/<int:invoice_id>', methods=['POST', 'GET'], csrf=False, type='http', auth="user",
                website=True)

    def download_catalogue(self, **kw):

        record_id = kw['invoice_id']
        print(kw['invoice_id'])
        """In this function we are calling the report template
        of the corresponding product and
        downloads the catalogue in pdf format"""

        pdf, _ = request.env.ref('cus_report.report_admission_challan').sudo()._render_qweb_pdf(
            [int(record_id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition', 'catalogue' + '.pdf;')]
        return request.make_response(pdf, headers=pdfhttpheaders)

class inheritinvoices(models.Model):
    _inherit="account.move"
  

    unpaid_inv_ids = fields.Many2many(
        comodel_name='account.move',
        compute='_compute_unpaid_invoice',
        string='UnPaid Invoice Ids',
        
    )

    due_day_text=fields.Char(string="Due Day",compute='_compute_remaining_days')
    due_day=fields.Integer(string="Due Day Num",compute='_compute_remaining_days')
    account_identifier=fields.Char(string="Account Identifier")

    def _compute_unpaid_invoice(self):
        
        for rec in self:
            rec.unpaid_inv_ids=self.env['account.move'].search([("move_type","=","out_invoice"),("partner_id","=",rec.partner_id.id),("payment_state","=","not_paid")])
           
    def _compute_remaining_days(self):
       
        for rec in self:
            rec.due_day=0
            rec.due_day_text=""
            if rec.invoice_date_due:
                d1 = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
                d2 = datetime.strptime(str(rec.invoice_date_due), "%Y-%m-%d")
                delta = d1 - d2
                rec["due_day"]=delta.days
                if delta.days>0:
                    rec["due_day_text"]="Outstanding"
                else:
                    rec["due_day_text"]=""
                
               

    
