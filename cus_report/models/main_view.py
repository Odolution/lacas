# import datetime
# from re import U

from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import http
from odoo.http import request
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
