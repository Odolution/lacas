# -*- coding: utf-8 -*-

from odoo import models, fields


class Relationships(models.Model):
    _inherit = 'school.student.relationship'

    invoice_recipient = fields.Boolean(string="Invoice recipient")
