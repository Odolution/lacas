from odoo import models, fields, api

class Difference_Bills(models.Model):
    _inherit = 'account.move'
    # _name = 'difference'
    difference = fields.Float(string="Difference", compute='_compute_difference', digits=(10,2))

    @api.depends('net_amount', 'amount_total_signed')
    def _compute_difference(self):
        for record in self:
            record['difference'] = False
            if record.net_amount != '' and record.amount_total_signed != '':
                record['difference'] = float(record.net_amount) - float(record.amount_total_signed)