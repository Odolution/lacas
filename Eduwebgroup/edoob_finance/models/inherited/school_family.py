# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api
from odoo.exceptions import ValidationError, MissingError


class Family(models.Model):
    _inherit = 'school.family'

    filter_invoice_address_allow = fields.Selection(
        selection=[
            ('individual', "Parents only"),
            ('students', "Students"),
            ('all', "All"),
            ], required=True, default='individual'
        )
    invoice_address_id = fields.Many2one('res.partner', ondelete='restrict')
    invoice_address_id_domain = fields.Char(compute='_compute_invoice_address_id_domain')

    @api.depends('filter_invoice_address_allow')
    def _compute_invoice_address_id_domain(self):
        for family in self:
            domain = []
            if self.filter_invoice_address_allow == 'students':
                domain = [('is_edoob_partner', '=', True), ('school_individual_ids.family_ids', '=', family._origin.id)]
            elif self.filter_invoice_address_allow == 'individual':
                domain = [('is_edoob_parent', '=', True), ('school_individual_ids.family_ids', '=', family._origin.id)]
            family.invoice_address_id_domain = json.dumps(domain)

    @api.model
    def create(self, vals):
        family = super(Family, self).create(vals)
        if not family.invoice_address_id:
            family._set_default_invoice_address()
        return family

    def write(self, vals):
        if 'invoice_address_id' not in vals and not self._context.get('skip_invoice_address_check', False):
            for family in self:
                if not family.invoice_address_id:
                    family._set_default_invoice_address()
        return super(Family, self).write(vals)

    def _set_default_invoice_address(self):
        for family in self:
            family.with_context(skip_invoice_address_check=True).write({'invoice_address_id': (family.individual_ids[:1].partner_id).id})
