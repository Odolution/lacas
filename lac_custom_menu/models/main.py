from odoo import models, api, fields, _
from odoo.exceptions import UserError

class field_changes_custom_update(models.Model):
    _inherit = 'account.move'
    udid_new_lv = fields.Char(string="UDID")
    facts_id_new_lv = fields.Char(string="Facts Id")
#     adm_amount=fields.Char(string="Admission Amount")
#     security_amount=fields.Char(string="Security Amount")
    std_dob=fields.Char(string="Date Of Birth")

    @api.onchange('x_student_id_cred',"student_ids")
    def _studentsbill_onchange(self):
#         self.udid_new_lv=''
#         self.facts_id_new_lv=" "
# #         self.adm_amount=""
# #         self.security_amount=' '
#         self.std_dob=' '

        if self.student_ids:
            self.udid_new_lv=self.student_ids.facts_udid
            self.facts_id_new_lv=self.student_ids.facts_id
            # self.adm_amount=self.student_ids.school_ids.name
            self.std_dob=self.student_ids.date_of_birth
            # self.security_amount=self.invoice_date_due

#         if self.invoice_line_ids:
#             for line in self.invoice_line_ids: 
#                 if 'Admission' in line.product_id.name:
#                     self.adm_amount=line.price_subtotal
#                 elif 'Security' in line.product_id.name:
#                     self.security_amount=line.price_subtotal
        
   
