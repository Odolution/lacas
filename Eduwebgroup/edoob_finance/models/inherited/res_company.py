# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    edoob_finance_split_by_student = fields.Boolean(string="Split charges by students")
