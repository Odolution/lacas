from odoo import models, fields, api
from odoo.exceptions import UserError

class account_inherit(models.Model):
    _inherit = "account.move"

    ten_subject_charges = fields.Integer(string="10_Subject_Charges",compute='_compute_charges')
    It_charges = fields.Integer(string="IT Charges",compute='_compute_charges')

    @api.depends('invoice_line_ids')
    def _compute_charges(self):
        ten_charges = 0
        it_charges = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.product_id.name == '10th Subject Charges':
                    ten_charges += line.price_total
                if line.product_id.name == "IT Charges":
                    it_charges += line.price_total

        self.ten_subject_charges = ten_charges
        self.It_charges = it_charges