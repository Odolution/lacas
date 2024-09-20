from odoo import models, fields, api
from odoo.exceptions import UserError

class TuitionTemplate(models.Model):
    _inherit = 'tuition.template'

    grade_level_ids = fields.Many2many('school.grade.level', string='Grade Levels')