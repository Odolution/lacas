from odoo import models, api, fields, _
from odoo.exceptions import UserError
# import json
# import datetime


class add_tution_plan_wiz(models.TransientModel):
    _name='add.tution.plan.wiz'

    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    # tution_template_id = fields.Many2one('tution.template', string='Tution Template')
    



