# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.fields import Command

class AccountMove(models.Model):
    _inherit = 'account.move'

    tuition_plan_ids = fields.Many2many(
        'tuition.plan', readonly=True, string="Tuition plans", store=True, relation='tuition_plan_account_move_rel', column1='account_move_id', column2='tuition_plan_id')
    student_ids = fields.Many2many(
        'school.student', readonly=True, string="Students", store=True, compute='compute_edoob_fields')
    family_id = fields.Many2one('school.family', string="Family")
    installment_real_date = fields.Date(string="Installment real date", help="This field is used to know if an installment has already generated an invoice")
    program_ids = fields.Many2many('school.program', compute='compute_edoob_school_structure', store=True)
    school_ids = fields.Many2many('school.school', compute='compute_edoob_school_structure', store=True)
    district_ids = fields.Many2many('school.district', compute='compute_edoob_school_structure', store=True)
    grade_level_ids = fields.Many2many('school.grade.level', compute='compute_edoob_school_structure', store=True)

    @api.depends('line_ids', 'line_ids.student_id')
    def compute_edoob_fields(self):
        for move in self:
            move.student_ids = move.line_ids.mapped('student_id')
        self.compute_edoob_school_structure()

    @api.depends('student_ids', 'student_ids.program_ids', 'student_ids.grade_level_ids', 'student_ids.school_ids', 'student_ids.district_ids')
    def compute_edoob_school_structure(self):
        for move in self:
            students = move.mapped('student_ids')
            move.program_ids = students.mapped('program_ids')
            move.grade_level_ids = students.mapped('grade_level_ids')
            move.school_ids = students.mapped('school_ids')
            move.district_ids = students.mapped('district_ids')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    tuition_plan_id = fields.Many2one('tuition.plan', string="Tuition plan")
    student_id = fields.Many2one('school.student', string="Student")
