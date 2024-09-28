# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.fields import Command
import json
from odoo.exceptions import ValidationError, MissingError

from odoo.tools import float_compare


# account.move 

class AccountMove(models.Model):
    _inherit = 'account.move'

    tuition_plan_ids = fields.Many2many(
        'tuition.plan', readonly=True, string="Tuition plans", store=True, relation='tuition_plan_account_move_rel', column1='account_move_id', column2='tuition_plan_id')
    student_ids = fields.Many2many(
        'school.student', readonly=True, string="Students", store=True, compute='compute_ol_fields')
    family_id = fields.Many2one('school.family', string="Family")
    installment_real_date = fields.Date(string="Installment real date", help="This field is used to know if an installment has already generated an invoice")
    program_ids = fields.Many2many('school.program', compute='compute_ol_school_structure', store=True)
    school_ids = fields.Many2many('school.school', compute='compute_ol_school_structure', store=True)
    district_ids = fields.Many2many('school.district', compute='compute_ol_school_structure', store=True)
    grade_level_ids = fields.Many2many('school.grade.level', compute='compute_ol_school_structure', store=True)

    @api.depends('line_ids', 'line_ids.student_id')
    def compute_ol_fields(self):
        for move in self:
            move.student_ids = move.line_ids.mapped('student_id')
        self.compute_ol_school_structure()

    @api.depends('student_ids', 'student_ids.program_ids', 'student_ids.grade_level_ids', 'student_ids.school_ids', 'student_ids.district_ids')
    def compute_ol_school_structure(self):
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

#product.category

class ProductCategory(models.Model):
    _inherit = 'product.category'

    district_id = fields.Many2one('school.district', string="School district")
    district_code = fields.Char(string="School district code", related='district_id.code')

#relationship

class Relationships(models.Model):
    _inherit = 'school.student.relationship'

    invoice_recipient = fields.Boolean(string="Invoice recipient")

#res.company

class ResCompany(models.Model):
    _inherit = 'res.company'

    ol_finance_split_by_student = fields.Boolean(string="Split charges by students")

#res.config.setting

class ResConfigSettings(models.TransientModel):
    """  Settings for school base module """
    _inherit = "res.config.settings"

    ol_finance_split_by_student = fields.Boolean(related='company_id.ol_finance_split_by_student', readonly=False)

# sale.order

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tuition_plan_ids = fields.Many2many(
        'tuition.plan', readonly=True, string="Tuition plans", store=True,
        relation='tuition_plan_sale_order_rel', column1='sale_order_id', column2='tuition_plan_id')
    ol_finance_journal_id = fields.Many2one('account.journal')
    student_ids = fields.Many2many('school.student', readonly=True, string="Students", store=True, compute='_compute_student_ids')
    family_id = fields.Many2one('school.family', string="Family")
    installment_real_date = fields.Date(string="Installment real date", help="This field is used to know if an installment has already generated an invoice")
    program_ids = fields.Many2many('school.program', compute='compute_school_structure', store=True)
    school_ids = fields.Many2many('school.school', compute='compute_school_structure', store=True)
    district_ids = fields.Many2many('school.district', compute='compute_school_structure', store=True)
    grade_level_ids = fields.Many2many('school.grade.level', compute='compute_school_structure', store=True)

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.ol_finance_journal_id:
            invoice_vals["journal_id"] = self.ol_finance_journal_id.id
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

# school.district 

class SchoolDistrict(models.Model):
    _inherit = 'school.district'

    product_category_ids = fields.One2many('product.category', 'district_id', string="Product categories")


# school.family

class Family(models.Model):
    _inherit = 'school.family'

    filter_invoice_address_allow = fields.Selection(
        selection=[
            ('individual', "Parents only"),
            ('students', "Students"),
            ('all', "All"),
            ], required=True, default='individual'
        )
    invoice_address_id_domain = fields.Char(compute='_compute_invoice_address_id_domain')

    @api.depends('filter_invoice_address_allow')
    def _compute_invoice_address_id_domain(self):
        for family in self:
            domain = []
            if self.filter_invoice_address_allow == 'students':
                domain = [('is_ol_partner', '=', True), ('school_individual_ids.family_ids', '=', family._origin.id)]
            elif self.filter_invoice_address_allow == 'individual':
                domain = [('is_ol_parent', '=', True), ('school_individual_ids.family_ids', '=', family._origin.id)]
            family.invoice_address_id_domain = json.dumps(domain)

    @api.model
    def create(self, vals):
        family = super(Family, self).create(vals)
        if not family.invoice_address_id:
            family._set_default_invoice_address()
        return family

    def write(self, vals):
        if 'invoice_address_id' not in vals and not self._context.get('skip_invoice_address_check', False):
            for family in self:
                if not family.invoice_address_id:
                    family._set_default_invoice_address()
        return super(Family, self).write(vals)

    def _set_default_invoice_address(self):
        for family in self:
            family.with_context(skip_invoice_address_check=True).write({'invoice_address_id': (family.individual_ids[:1].partner_id).id})


# school.student

class Student(models.Model):
    _inherit = 'school.student'

    tuition_plan_ids = fields.One2many('tuition.plan', 'student_id', string="Tuition plans")
    tuition_plan_count = fields.Integer(string="Tuition plan count", compute='compute_tuition_plan_count')
    financial_responsibility_ids = fields.One2many(
        'school.financial.responsibility', 'student_id',
        string="Financial responsibilities")

    # Concession tab

    concession_line_ids     =   fields.One2many('concession.plan.line', 'student_id', string="Concession Line")

    def add_discount_plan(self):
        # raise ValidationError(str(self.tuition_plan_ids))

        for plan in self.tuition_plan_ids:

            installment_obj = plan.line_ids[-1].installment_ids
            line_concession_list = plan.student_id.concession_line_ids.get_concession_values(installment_obj)
            line_concession_list = [Command.create(vals) for vals in line_concession_list]

            raise ValidationError(str(line_concession_list))

        

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
        action = self.env['ir.actions.actions']._for_xml_id('ol_school_account.tuition_plan_action')
        if len(tuition_plans) > 1:
            action['domain'] = [('id', 'in', tuition_plans.ids)]
        elif len(tuition_plans) == 1:
            form_view = [(self.env.ref('ol_school_account.tuition_plan_view_form').id, 'form')]
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
