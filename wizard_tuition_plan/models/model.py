from odoo import models, api, fields


class wizard_tuition_plan(models.TransientModel):
    _name='tuition.wizard_tuition_plan'

    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    

    