# -*- coding:utf-8 -*-

from odoo import models, fields, api


class SincroDataAPI(models.Model):
    _name = "sincro_data_base.api"
    _description = "Sincro Data Request"

    method = fields.Char(string="Method")
    name = fields.Char(string="Name", required=True)
    base_url = fields.Char(string="Base URL", required=True)
    request_ids = fields.One2many("sincro_data_base.server", "api_id")
    header_ids = fields.Many2many("sincro_data_base.header", string="Headers")
