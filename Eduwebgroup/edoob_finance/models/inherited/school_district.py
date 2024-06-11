# -*- coding: utf-8 -*-

from odoo import models, fields


class SchoolDistrict(models.Model):
    _inherit = 'school.district'

    product_category_ids = fields.One2many('product.category', 'district_id', string="Product categories")
