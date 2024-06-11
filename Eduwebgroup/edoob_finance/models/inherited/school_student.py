# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, MissingError
from odoo.tools import float_compare


class Student(models.Model):
    _inherit = 'school.student'

    tuition_plan_ids = fields.One2many('tuition.plan', 'student_id', string="Tuition plans")
    tuition_plan_count = fields.Integer(string="Tuition plan count", compute='compute_tuition_plan_count')
    financial_responsibility_ids = fields.One2many(
        'school.financial.responsibility', 'student_id',
        string="Financial responsibilities")

    @api.constrains('financial_responsibility_ids')
    def _check_category_sum(self):
        for student in self:
            family_responsibilities = student.financial_responsibility_ids
            categories = family_responsibilities.mapped('product_category_id')
            for category in categories:
                responsibilities_by_categories = family_responsibilities.filtered(
                    lambda fr: fr.product_category_id == category)
                percentage_sum = sum(responsibilities_by_categories.mapped('percentage'))
                decimal_precision = self.env['decimal.precision'].precision_get('Finance responsibility percentage')
                if float_compare(percentage_sum, 1.0, precision_digits=decimal_precision):
                    raise ValidationError(
                        _("Student[%s]: %s Category: %s doesn't sum 100!",
                          student.id, student.name, category.complete_name))

    def get_individual_invoice_recipients(self, family_id: int):
        return (
            self.relationship_ids.
            filtered(lambda r: r.invoice_recipient and family_id in r.individual_id.family_ids.ids)
            .mapped('individual_id'))

    @api.depends('tuition_plan_ids')
    def compute_tuition_plan_count(self):
        for template in self:
            template.tuition_plan_count = len(template.tuition_plan_ids)

    def action_view_tuition_plans(self):
        self.ensure_one()
        tuition_plans = self.tuition_plan_ids
        action = self.env['ir.actions.actions']._for_xml_id('edoob_finance.tuition_plan_action')
        if len(tuition_plans) > 1:
            action['domain'] = [('id', 'in', tuition_plans.ids)]
        elif len(tuition_plans) == 1:
            form_view = [(self.env.ref('edoob_finance.tuition_plan_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = tuition_plans.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


class FinancialResponsibility(models.Model):
    _name = 'school.financial.responsibility'
    _description = "School financial responsibility"

    student_id = fields.Many2one('school.student', string="Student", required=True, ondelete='cascade')
    student_family_ids = fields.Many2many('school.family', string="Student families", related='student_id.family_ids')
    family_id = fields.Many2one('school.family', required=True, ondelete='cascade')

    product_category_id = fields.Many2one('product.category', string="Category", required=True, ondelete='cascade')
    percentage = fields.Float(string="Percentage (%)", digits="Finance responsibility percentage", required=True, default=1)
