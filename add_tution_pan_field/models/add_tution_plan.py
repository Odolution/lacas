from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime


class add_tution_plan_wiz(models.TransientModel):
    _name='tuition.add_tution_plan_wiz'

    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    



