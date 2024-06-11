# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    district_id = fields.Many2one('school.district', string="School district")
    district_code = fields.Char(string="School district code", related='district_id.code')
