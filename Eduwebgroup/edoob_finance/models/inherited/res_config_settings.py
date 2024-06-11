# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    """  Settings for school base module """
    _inherit = "res.config.settings"

    edoob_finance_split_by_student = fields.Boolean(related='company_id.edoob_finance_split_by_student', readonly=False)