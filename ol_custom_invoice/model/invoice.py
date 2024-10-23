from odoo import models, api, fields, _
from odoo.exceptions import UserError

class InheritInvoice(models.Model):
    _inherit = 'account.move'

    robotic_charges = fields.Float('Robotic Charges',compute='_compute_charges')

    @api.depends('invoice_line_ids')
    def _compute_charges(self):
        robotic_charges = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.product_id.name == 'Robotics':
                    robotic_charges += line.price_unit
        
        self.robotic_charges = robotic_charges
