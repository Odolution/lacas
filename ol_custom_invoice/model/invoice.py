from odoo import models, api, fields, _
from odoo.exceptions import UserError

class InheritInvoice(models.Model):
    _inherit = 'account.move'

    robotic_charges = fields.Float('Robotic Charges',compute='_compute_charges',store=True)
    parent_day_charges = fields.Float('Parents Day Charges',compute='_compute_charges',store=True)

    def _compute_charges(self):
        robotic_charges = 0
        parent_day_charges = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.product_id.name == 'Robotics':
                    robotic_charges += line.price_unit
                if line.product_id.name == 'Parents Day':
                    parent_day_charges += line.price_unit
        
        self.robotic_charges = robotic_charges
        self.parent_day_charges = parent_day_charges
