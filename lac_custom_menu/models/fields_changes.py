from odoo import models, api, fields, _
from odoo.exceptions import UserError

class field_changes_custom_update(models.Model):
    _inherit = 'account.move'
    udid_new_lv = fields.Char(string="UDID NEW")

    
    