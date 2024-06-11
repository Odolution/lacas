# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.fields import Command


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tuition_plan_ids = fields.Many2many(
        'tuition.plan', readonly=True, string="Tuition plans", store=True,
        relation='tuition_plan_sale_order_rel', column1='sale_order_id', column2='tuition_plan_id')
    edoob_finance_journal_id = fields.Many2one('account.journal')
    student_ids = fields.Many2many('school.student', readonly=True, string="Students", store=True, compute='_compute_student_ids')
    family_id = fields.Many2one('school.family', string="Family")
    installment_real_date = fields.Date(string="Installment real date", help="This field is used to know if an installment has already generated an invoice")
    program_ids = fields.Many2many('school.program', compute='compute_school_structure', store=True)
    school_ids = fields.Many2many('school.school', compute='compute_school_structure', store=True)
    district_ids = fields.Many2many('school.district', compute='compute_school_structure', store=True)
    grade_level_ids = fields.Many2many('school.grade.level', compute='compute_school_structure', store=True)

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.edoob_finance_journal_id:
            invoice_vals["journal_id"] = self.edoob_finance_journal_id.id
        if self.tuition_plan_ids:
            invoice_vals.update({
                'family_id': self.family_id.id,
                })

        return invoice_vals

    @api.depends('order_line.student_id')
    def _compute_student_ids(self):
        for order in self:
            order.student_ids = order.mapped('order_line.student_id')
        self.compute_school_structure()

    @api.depends('student_ids', 'student_ids.program_ids', 'student_ids.grade_level_ids', 'student_ids.school_ids', 'student_ids.district_ids')
    def compute_school_structure(self):
        for order in self:
            students = order.mapped('student_ids')
            order.program_ids = students.mapped('program_ids')
            order.grade_level_ids = students.mapped('grade_level_ids')
            order.school_ids = students.mapped('school_ids')
            order.district_ids = students.mapped('district_ids')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tuition_plan_id = fields.Many2one('tuition.plan', string="Tuition plan")
    student_id = fields.Many2one('school.student', string="Student")

    def _prepare_invoice_line(self, **optional_values):
        values = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        values['student_id'] = self.student_id.id
        values['tuition_plan_id'] = self.tuition_plan_id.id
        if optional_values:
            values.update(optional_values)
        return values
