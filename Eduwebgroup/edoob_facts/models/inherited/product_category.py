# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    facts_id = fields.Integer(string="Facts id")
    facts_school_code = fields.Char("Facts school code")
