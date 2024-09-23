from odoo import models, fields, api
from odoo.exceptions import UserError

class TuitionTemplate(models.Model):
    _inherit = 'tuition.template'
    
    program_id = fields.Many2one('school.program', string='Program')
    grade_level_ids = fields.Many2many('school.grade.level', string='Grade Levels',  
    domain= [('program_id', '=', program_id.id)])

    # @api.onchange('program_id')
    # def _onchange_program_id(self):
    #     if self.program_id:
    #         return {
    #             'domain': {
    #                 'grade_level_ids': [('program_id', '=', self.program_id.id)]
    #             }
    #         }
    #     else:
    #         return {
    #             'domain': {
    #                 'grade_level_ids': []
    #             }
    #         }

