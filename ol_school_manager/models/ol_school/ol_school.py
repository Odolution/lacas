# -*- coding: utf-8 -*-

"""
Author: Luis Malavé
Date: 2021-04-05
Yes, I know that Odoo tips say dont do this...
But... I am just grouping things together to get some kind of order without
modifying the __init__ over and over again...
"""

from odoo import models, fields, api, _
import datetime
from odoo.exceptions import UserError
from odoo import exceptions
from odoo.exceptions import ValidationError
import datetime
from odoo.fields import Command
# X2M methods codes
from odoo.osv import expression

# school.relaed.model
class SchoolBasePartnerCurrentSchoolGrade(models.Model):
    """ It is used as M:N table """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.partner.current.school.grade'
    _description = "Partner current school grade"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    partner_id = fields.Many2one('res.partner', required=True)
    school_id = fields.Many2one('school.school', required=True)
    program_id = fields.Many2one('school.program', required=True)
    grade_level_id = fields.Many2one('school.grade.level', required=True)

    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################
    _sql_constraints = [
        ('unique_partner_grade_level_relation',
         'unique(partner_id,school_id,program_id, grade_level_id)',
         'Error, a partner cannot have repeated grade level program relation'),
        ]
    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################


class SchoolBasePartnerNextSchoolGrade(models.Model):
    """ It is used as M:N table """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.partner.next.school.grade'
    _description = "Partner next school grade"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    partner_id = fields.Many2one('res.partner')
    school_id = fields.Many2one('school.school')
    grade_level_id = fields.Many2one('school.grade.level')

    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################


class SchoolBaseGradeLevelType(models.Model):
    _name = 'school.grade.level.type'
    _description = "Grade level type"

    type = fields.Selection([
        ('elementary', _("Elementary")),
        ('middle_school', _("Middle school")),
        ('high_school', _("High school")),
        ], required=True)
    name = fields.Char(required=True)


class Placement(models.Model):
    """ An informative model for students """
    _name = 'school.placement'
    _description = "Placement"
    name = fields.Char(string="Placement", required=True, translate=True)
    key = fields.Char(string="Key")


class WithdrawReason(models.Model):
    """ Why does the student withdraw? """
    _name = 'school.withdraw_reason'
    _description = "Withdraw reasons"
    name = fields.Char(string="WithDraw Reason", required=True, translate=True)
    key = fields.Char(string="Key")

    def testg(self):
        pass


class MaritalStatus(models.Model):
    """ An informative model for students """
    _name = 'school.marital_status'
    _description = "Marital Status"
    name = fields.Char(string="Name", required=True, translate=True)
    key = fields.Char(string="Key")


class Gender(models.Model):
    _name = "school.gender"
    _description = "School gender"
    name = fields.Char("Gender", required=True, translate=True)
    key = fields.Char("Key")

#ser.vice

class Service(models.Model):
    _name = "school.service"
    _description = "School Service"

    name = fields.Char(string="Name")

#academic.enrollment.history

class SchoolEnrollmentHistory(models.Model):
    _name = 'school.enrollment.history'
    _description = "Enrollment history"
    _order = 'timestamp DESC'

    student_id = fields.Many2one('school.student', string="Student", ondelete='set null')
    student_name = fields.Char()

    program_id = fields.Many2one(
        'school.program', string="Current program", required=True, default=lambda self: self.env.program)
    school_id = fields.Many2one('school.school', string="Current school", related='program_id.school_id')
    grade_level_id = fields.Many2one(
        'school.grade.level', string="Grade level",
        domain="[('program_id', '=', program_id)]")
    enrollment_status_id = fields.Many2one('school.enrollment.status', string="Current status", required=True)
    enrollment_sub_status_id = fields.Many2one(
        'school.enrollment.sub.status',
        domain="[('program_id', '=', program_id), ('status_id', '=', enrollment_status_id)]",
        string="Current sub status"
        )

    next_school_id = fields.Many2one('school.school', string="Next school", related='next_program_id.school_id')
    next_program_id = fields.Many2one('school.program', string="Next program", default=lambda self: self.env.program)
    next_grade_level_id = fields.Many2one(
        'school.grade.level', string="Next grade level",
        domain="[('program_id', '=', program_id)]")
    next_enrollment_status_id = fields.Many2one('school.enrollment.status', string="Next status")
    next_enrollment_sub_status_id = fields.Many2one(
        'school.enrollment.sub.status',
        domain="[('program_id', '=', next_program_id), ('status_id', '=', next_enrollment_status_id)]",
        string="Next sub status")

    enrolled_date = fields.Date(string="Enrolled date")
    graduation_date = fields.Date(string="Graduation date")
    withdraw_date = fields.Date(string="Withdraw date")

    timestamp = fields.Datetime(string="Date", required=True, default=fields.Datetime.now())
    note = fields.Char(string="Note")

    @api.constrains('enrollment_sub_status_id')
    def check_enrollment_sub_status_id(self):
        for record in self:
            sub_status = record.enrollment_sub_status_id
            status = record.enrollment_status_id
            if sub_status and sub_status.status_id != status:
                raise ValidationError(_("Sub status %s belong to %s", sub_status.name, status.name))

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.student_name = res.student_id.name
        return res

#academic.student.enrollment.state

class StudentEnrollState(models.Model):
    _name = 'school.student.enrollment.state'
    _description = "Student enrollment state"

    student_id = fields.Many2one('school.student', string="Student", required=True, ondelete='cascade')

    program_id = fields.Many2one('school.program', string="Current program", required=True)
    school_id = fields.Many2one('school.school', string="Current school", related='program_id.school_id')
    grade_level_id = fields.Many2one('school.grade.level', string="Grade level", domain="[('program_id', '=', program_id)]")
    enrollment_status_id = fields.Many2one('school.enrollment.status', string="Current status", required=True)
    enrollment_sub_status_id = fields.Many2one(
        'school.enrollment.sub.status',
        domain="[('program_id', '=', program_id), ('status_id', '=', enrollment_status_id)]",
        string="Current sub status"
        )

    next_program_id = fields.Many2one('school.program', string="Next program")
    next_school_id = fields.Many2one('school.school', string="Next school", related='next_program_id.school_id')
    next_grade_level_id = fields.Many2one(
        'school.grade.level', string="Next grade level",
        domain="[('program_id', '=', next_program_id)]")
    next_enrollment_status_id = fields.Many2one('school.enrollment.status', string="Next status")
    next_enrollment_sub_status_id = fields.Many2one(
        'school.enrollment.sub.status',
        domain="[('program_id', '=', next_program_id), ('status_id', '=', next_enrollment_status_id)]",
        string="Next sub status"
        )

    enrolled_date = fields.Date(string="Enrolled date")
    graduation_date = fields.Date(string="Graduation date")
    withdraw_date = fields.Date(string="Withdraw date")
    note = fields.Text(string="Note")

    _sql_constraints = [
        ('student_program_unique',
         'unique(student_id, program_id)',
         "You cannot have more than one enrollment state for the same student in the same program"),
        ]

    @api.model
    def create(self, vals):
        enrollment_state = super().create(vals)
        enrollment_state._log_action()
        return enrollment_state

    def write(self, vals):
        res = super().write(vals)
        if res:
            self._log_action()
        return res

    def _log_action(self):
        for enrollment_state in self:
            enrollment_history_values = enrollment_state._prepare_enrollment_history_values()
            self.env['school.enrollment.history'].create(enrollment_history_values)

    def _prepare_enrollment_history_values(self):
        self.ensure_one()
        return {
            'student_id': self.student_id.id,
            'program_id': self.program_id.id,
            'grade_level_id': self.grade_level_id.id,
            'enrollment_status_id': self.enrollment_status_id.id,
            'enrollment_sub_status_id': self.enrollment_sub_status_id.id,

            'next_program_id': self.next_program_id.id,
            'next_grade_level_id': self.next_grade_level_id.id,
            'next_enrollment_status_id': self.next_enrollment_status_id.id,
            'next_enrollment_sub_status_id': self.next_enrollment_sub_status_id.id,

            'enrolled_date': self.enrolled_date,
            'graduation_date': self.graduation_date,
            'withdraw_date': self.withdraw_date,

            'timestamp': fields.Datetime.now(),
            }

    @api.onchange('enrollment_status_id')
    def onchange_enrollment_status_id(self):
        self.enrollment_sub_status_id = False

    @api.onchange('program_id')
    def onchange_enrollment_program_id(self):
        self.grade_level_id = False
        self.enrollment_status_id = False
        self.enrollment_sub_status_id = False

    @api.onchange('enrollment_status_id')
    def onchange_enrollment_next_status_id(self):
        self.next_enrollment_sub_status_id = False

    @api.onchange('next_program_id')
    def onchange_enrollment_next_program_id(self):
        self.next_grade_level_id = False
        self.next_enrollment_status_id = False
        self.next_enrollment_sub_status_id = False

    ###############
    # Constraints #
    ###############
    @api.constrains('enrollment_sub_status_id')
    def check_enrollment_sub_status_id(self):
        for record in self:
            sub_status = record.enrollment_sub_status_id
            program = record.program_id
            status = record.enrollment_status_id
            if sub_status:
                if sub_status.status_id != status:
                    raise ValidationError(_("Sub status %s doesn't belong to %s", sub_status.name, status.name))
                elif sub_status.program_id != program:
                    raise ValidationError(_("Sub status %s doesn't belong to %s", sub_status.name, program.name))

    @api.constrains('enrollment_sub_status_id')
    def check_enrollment_sub_status_id(self):
        for record in self:
            sub_status = record.enrollment_sub_status_id
            status = record.enrollment_status_id
            if sub_status and sub_status.status_id != status:
                raise ValidationError(_("Sub status %s belong to %s", sub_status.name, status.name))

    @api.constrains('enrollment_sub_status_id')
    def check_enrollment_sub_status_id(self):
        for record in self:
            sub_status = record.enrollment_sub_status_id
            status = record.enrollment_status_id
            if sub_status and sub_status.status_id != status:
                raise ValidationError(_("Sub status %s belong to %s", sub_status.name, status.name))

#health.care.allergy

class Allergy(models.Model):
    _name = "school.allergy"
    _description = "Allergies for contacts (students or somebody else)"

    name = fields.Char("Name")
    description = fields.Char("Description")
    partner_id = fields.Many2one("res.partner", "Contact")
    olf_id = fields.Integer('olf Id')

    @api.constrains('olf_id')
    def check_unique_olf_id(self):
        for allergy in self:
            if allergy.olf_id and allergy.search_count([('olf_id', '=', allergy.olf_id)]) > 1:
                raise exceptions.ValidationError(_('There exists an codition with the same olf id [%s]' % allergy.olf_id))

#health.care.conditions

class Condition(models.Model):
    _name = "school.condition"
    _description = "Conditions for contacts (students or somebody else)"

    name = fields.Char("Name")
    description = fields.Char("Description")
    partner_id = fields.Many2one("res.partner", "Contact")
    olf_id = fields.Integer('olf Id')

    @api.constrains('olf_id')
    def check_unique_olf_id(self):
        for condition in self:
            if condition.olf_id and condition.search_count([('olf_id', '=', condition.olf_id)]) > 1:
                raise exceptions.ValidationError(_('There exists an codition with the same olf id [%s]' % condition.olf_id))

#health.care.health.care.allergy

class SchoolBaseMedicalAllergy(models.Model):
    _name = 'school.healthcare.allergy'
    _description = "Medical allergy"

    name = fields.Char("Name")
    comment = fields.Char("Comment")

    partner_id = fields.Many2one("res.partner", string="Partner")

#health.care.condition

class SchoolBaseMedicalCondition(models.Model):
    _name = 'school.healthcare.condition'
    _description = "Medical condition"

    name = fields.Char("Name")
    comment = fields.Char("Comment")
    
    partner_id = fields.Many2one("res.partner", string="Partner")

#health.care.medication

class SchoolBaseMedicalMedication(models.Model):
    _name = 'school.healthcare.medication'
    _description = "Medical medication"

    name = fields.Char("Name")
    comment = fields.Char("Comment")
    
    partner_id = fields.Many2one("res.partner", string="Partner")

#people.management.enrollment.status

class EnrollmentStatus(models.Model):
    """ Enrollment for students """
    _name = 'school.enrollment.status'
    _description = "Enrollment Status"
    name = fields.Char(string="Name", required=True, translate=True)
    key = fields.Char(
        string="Key", 
        help="This is used mainly for web services")
    note = fields.Char(string="Description")
    type = fields.Selection([
        ('enrolled', 'Enrolled'),
        ('withdrawn', 'Withdrawn'),
        ('graduate', 'Graduate'),
        ('pre-enrolled', 'Pre-Enrolled'),
        ('inactive', 'Inactive'),
        ('admissions', 'Admissions'),
        ])
    sub_status_ids = fields.One2many('school.enrollment.sub.status', 'status_id')
    reference_id = fields.Char('Enrollment Status Reference ID')


class EnrollmentSubStatus(models.Model):
    """ Substatus for students """
    _name = 'school.enrollment.sub.status'
    _description = "Enrollment sub status"

    status_id = fields.Many2one('school.enrollment.status', string='Status')
    program_id = fields.Many2one('school.program', required=True, default=lambda self: self.env.program)
    name = fields.Char(string="Name", required=True, translate=True)
    key = fields.Char(string="Key")
    reference_id = fields.Char('Enrollment Sub Status Reference ID')

#people.management.family.individual

class SchoolBaseIndividual(models.Model):
    """ School Family Individual """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.family.individual'
    _description = "Family individual"
    _inherits = {
        'res.partner': 'partner_id',
        }
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    ###################
    # Default methods #
    ###################
    @api.model
    def _default_login(self):
        import time
        return 'individual%i' % int(time.time())

    ######################
    # Fields declaration #
    ######################
    partner_name = fields.Char(
        store=True, compute="_compute_name", inverse='_set_name', string="Contact name")

    user_id = fields.Many2one('res.users', string="User")
    partner_id = fields.Many2one('res.partner', required=True, readonly=False, ondelete='restrict', string="Related contact")

    active = fields.Boolean(default=True)

    first_name = fields.Char(required=True)
    middle_name = fields.Char()
    last_name = fields.Char(required=True)

    family_ids = fields.Many2many(
        'school.family',
        relation='individual_family_rel',
        column1='individual_id',
        column2='family_id', required=True, string="Families")
    family_student_ids = fields.Many2many(
        'school.student', string="Family Students",
        help="This are the students in the family",
        related='family_ids.student_ids')

    is_student = fields.Boolean(string="Is student", compute='compute_is_student', store=True)
    student_ids = fields.One2many('school.student', 'individual_id', string="Students (Technical)")
    family_student_ids = fields.Many2many('school.student', store=False, readonly=True, compute='compute_family_students')
    family_individual_ids = fields.Many2many(related='family_ids.individual_with_students_ids', string="Family individuals")

    relationship_ids = fields.One2many('school.student.relationship', 'individual_id', string="Relationships", readonly=False)

    # Demographics
    date_of_birth = fields.Date(string="Date of birth")
    gender = fields.Many2one('school.gender', string="Gender")
    email2 = fields.Char("Email 2")

    reference_id = fields.Char('Family Individual Reference ID')

    citizenship = fields.Char(string='Citizenship')
    ethnicity = fields.Char(string='Ethnicity')
    race = fields.Char(string='Race')

    ##############################
    # Compute and search methods #
    ##############################
    @api.depends("first_name", "middle_name", "last_name")
    def _compute_name(self):
        self.auto_format_name()

    @api.onchange("first_name", "middle_name", "last_name")
    def onchange_individual_name(self):
        self.auto_format_name()

    def _set_name(self):
        for individual in self:
            individual.partner_id.name = individual.partner_name

    @api.depends('student_ids')
    def compute_is_student(self):
        for individual in self:
            individual.is_student = bool(individual.student_ids)

    @api.depends('family_ids', 'family_ids.student_ids')
    def compute_family_students(self):
        for individual in self:
            individual.family_student_ids = individual.mapped('family_ids.student_ids') - individual.student_ids

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################
    def write(self, values):
        self._add_name_in_values_in_proper_format(values)
        res = super(SchoolBaseIndividual, self).write(values)
        self._fields_sync()
        return res

    @api.model
    def create(self, values):
        self._add_name_in_values_in_proper_format(values)
        res = super(SchoolBaseIndividual, self).create(values)
        self._fields_sync()
        return res

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if not self.env.su and not self._context.get('no_program_filter', False):
            allowed_programs = self.env.programs.get_with_parent()
            program_domain = [
                '|', ('student_ids', '=', False),
                '&', ('student_ids', '!=', False),
                '|', ('student_ids.program_ids', '=', False), ('student_ids.program_ids', 'in', allowed_programs.ids)]
            search_domain = expression.AND([program_domain, args])
        else:
            search_domain = args
        return super()._search(search_domain, offset, limit, order, count, access_rights_uid)
    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
    def _fields_sync(self):
        pass

    def _add_name_in_values_in_proper_format(self, values):
        if 'name' not in values and ('first_name' in values or 'middle_name' in values or 'last_name' in values):

            def _get_from_values_or_record(key):
                if key in values:
                    return values[key]
                elif self:
                    return self[key]
                else:
                    return ''

            first_name = _get_from_values_or_record('first_name')
            middle_name = _get_from_values_or_record('middle_name')
            last_name = _get_from_values_or_record('last_name')
            values["name"] = self.format_name(first_name, middle_name, last_name)

    def auto_format_name(self):
        """ Use format_name method to create that """
        for individual in self:
            first = individual.first_name
            middle = individual.middle_name
            last = individual.last_name

            if any([first, middle, last]):
                individual.partner_name = individual.format_name(first, middle,
                                                                 last)
                individual.name = individual.format_name(first, middle, last)
            else:
                individual.partner_name = individual.partner_name
                individual.name = individual.name

    @api.model
    def format_name(self, first_name, middle_name, last_name):
        """
        This will format everything depending of school settings
        :return: A String with the formatted version
        """

        name_order_relation = {
            self.env.ref("ol_school_manager.name_sorting_first_name"):
                first_name or "",
            self.env.ref(
                "ol_school_manager.name_sorting_middle_name"): middle_name or "",
            self.env.ref("ol_school_manager.name_sorting_last_name"): last_name or ""
            }

        name_sorting_ids = self.env.ref(
            "ol_school_manager.name_sorting_first_name") + self.env.ref(
            "ol_school_manager.name_sorting_middle_name") + self.env.ref(
            "ol_school_manager.name_sorting_last_name")

        name = ""
        sorted_name_sorting_ids = name_sorting_ids.sorted("sequence")
        for sorted_name_id in sorted_name_sorting_ids:
            name = f"{name}{sorted_name_id.prefix or ''}{name_order_relation.get(sorted_name_id, '')}{(sorted_name_id.suffix or '')}"

        return name

    def open_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'name': self.partner_name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            }

    def create_enroll_form_individuals(self):
        self.ensure_one()
        enroll_form_id = self._context.get('default_form_id', False)
        enroll_form = self.env['enroll.student.form'].browse(enroll_form_id)
        existing_individual_in_form = enroll_form.individual_ids.filtered(lambda ind: ind.real_individual_id == self)
        if existing_individual_in_form:
            return existing_individual_in_form.ids
        FormIndividualEnv = self.env['enroll.student.form.individual'].sudo()
        form_individual_ids = []
        for individual in self:
            values = individual._prepare_enroll_form_individual_values()
            form_individual = FormIndividualEnv.create(values)
            form_individual_ids.append(form_individual.id)
        return form_individual_ids

    def _prepare_enroll_form_individual_values(self):
        self.ensure_one()
        return {
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,

            'date_of_birth': self.date_of_birth,
            'gender': self.gender.id,
            'citizenship': self.citizenship,
            'ethnicity': self.ethnicity,
            'race': self.race,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': self.email,
            'email2': self.email2,

            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'state_id': self.state_id.id,
            'country_id': self.country_id.id,
            'real_individual_id': self.id,
            'form_id': self._context.get('default_form_id', False),
            }

#people.management.family

ACTION_TYPE = 0
TYPE_CREATE = 0
TYPE_REPLACE = 6
TYPE_ADD_EXISTING = 4
TYPE_REMOVE_NO_DELETE = 3
TYPE_REMOVE_DELETE = 2


class SchoolFamily(models.Model):

    ######################
    # Private Attributes #
    ######################
    _name = 'school.family'
    _description = "Family"
    _inherit = [
        'portal.mixin', 'mail.thread', 'mail.activity.mixin', 'avatar.mixin'
        ]

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char()
    active = fields.Boolean(default=True)
    
    invoice_address_id = fields.Many2one('res.partner', ondelete='restrict')

    individual_with_students_ids = fields.Many2many(
        'school.family.individual', string="All Individuals including students",
        relation='individual_family_rel',
        column1='family_id',
        column2='individual_id')

    student_ids = fields.Many2many(
        'school.student', string="Students",
        store=True, compute='compute_student_ids', inverse='_set_student_ids')
    individual_ids = fields.Many2many(
        'school.family.individual', string="Individuals",
        relation='individual_family_rel',
        column1='family_id',
        column2='individual_id', domain=[('is_student', '=', False)])

    # wizard related resource field
    student_wizard_ids = fields.Char(default='')
    reference_id = fields.Char('Family Reference ID')

    ##############################
    # Compute and search methods #
    ##############################
    @api.depends('individual_with_students_ids')
    def compute_student_ids(self):
        for family in self:
            family.student_ids = family.individual_with_students_ids.student_ids
            family.individual_ids = family.individual_with_students_ids.filtered(lambda i: not i.student_ids)

    def _set_student_ids(self):
        for family in self:
            family.individual_with_students_ids += family.student_ids.mapped('individual_id')

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if not self.env.su and not self._context.get('no_program_filter', False):
            allowed_programs = self.env.programs.get_with_parent()
            program_domain = ['|', ('student_ids', '=', False), ('student_ids.program_ids', 'in', allowed_programs.ids)]
            search_domain = expression.AND([program_domain, args])
        else:
            search_domain = args
        return super(SchoolFamily, self)._search(search_domain, offset, limit, order, count, access_rights_uid)

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
    def open_family(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.family',
            'name': self.name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            }

    def prepare_enroll_form_family_default_values(self):
        self.ensure_one()
        individuals_values = [individual._prepare_enroll_form_individual_values() for individual in self.individual_ids]
        individuals = self.env['enroll.student.form.individual'].sudo().create(individuals_values)
        return {
            'name': self.name,
            'real_family_id': self.id,
            'individual_ids': [Command.set(individuals.ids)],
            'form_id': self._context.get('default_form_id', False),
            }

#people.management.relationship

class SchoolBaseRelationship(models.Model):
    _name = 'school.student.relationship'
    _description = "Student relationship"

    student_id = fields.Many2one("school.student", string="Student", required=True, ondelete="cascade")
    individual_id = fields.Many2one("school.family.individual", string="Individual", required=True, ondelete="cascade")
    relationship_type_id = fields.Many2one(
        'school.student.relationship.type', required=True, string="Relationship type",
        default=lambda self: self.env['school.student.relationship.type'].get_default_other_relationship()
        )

    custody = fields.Boolean(string="Custody")
    correspondence = fields.Boolean(string="Correspondence")
    grade_related = fields.Boolean(string="Grade Related")
    family_portal = fields.Boolean(string="Family Portal")
    is_emergency_contact = fields.Boolean("Emergency contact")


class RelationshipType(models.Model):
    """ SubStatus for students """
    _name = 'school.student.relationship.type'
    _description = "Relationship Type"
    _order = "sequence"

    @api.model
    def get_default_parent_relationship(self):
        return self.env.ref('ol_school_manager.relationship_parent', raise_if_not_found=False)

    @api.model
    def get_default_other_relationship(self):
        return self.env.ref('ol_school_manager.relationship_other', raise_if_not_found=False)

    name = fields.Char(string="Relationship type", required=True, translate=True)
    key = fields.Char(string="Key", translate=False)
    type = fields.Selection([
        ('daughter', _("Daughter")),
        ('son', _("Son")),
        ('child', _("Child")),

        ('sibling', _("Sibling")),
        ('brother', _("Brother")),
        ('sister', _("Sister")),

        ('parent', _("Parent")),
        ('father', _("Father")),
        ('mother', _("Mother")),

        ('grandparent', _("Grandparent")),
        ('grandmother', _("Grandmother")),
        ('grandfather', _("Grandfather")),

        ('stepparent', _("Stepparent")),
        ('stepmother', _("Stepmother")),
        ('stepfather', _("Stepfather")),
        ('stepsibling', _("Stepsibling")),
        ('stepsister', _("Stepsister")),
        ('stepbrother', _("Stepbrother")),

        ('uncle', _("Uncle")),
        ('cousin', _("Cousin")),
        ('other', _("Other")),
        ], string="Type")
    sequence = fields.Integer(default=1)

#people.management.student


class ConcessionLine(models.Model):
    _name = "consession.line"

    student_id = fields.Many2one('school.student', string="Student", ondelete='set null')

    discount_name    = fields.Many2one('ol.discount.charges', string="Discount name")
    discount_product = fields.Many2one('product.product', string="Discount Product")
    # month_ids        = fields.Many2many('tuition.installment', string="Month") 

class SchoolStudent(models.Model):
    """ Student model """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.student'
    _description = "Student"
    _inherits = {
        'school.family.individual': 'individual_id',
        }
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################

    # Demographics
    individual_id = fields.Many2one('school.family.individual', required=True, ondelete='restrict', string="Individual")
    student_status_id = fields.Many2one('school.enrollment.status')
    grade_level_id = fields.Many2one('school.grade.level')
    school_udid = fields.Char(string='School UDID')

    # Healthcare
    allergies_ids = fields.One2many("school.healthcare.allergy", "partner_id", string="Medical Allergies")
    conditions_ids = fields.One2many("school.healthcare.condition", "partner_id", string="Medical conditions")
    medications_ids = fields.One2many("school.healthcare.medication", "partner_id", string="Medical Medication")

    doctor_name = fields.Char("Doctor name")
    doctor_phone = fields.Char("Doctor phone")
    doctor_address = fields.Char("Doctor Direction")
    hospital = fields.Char("Hospital")
    hospital_address = fields.Char("Hospital Address")
    permission_to_treat = fields.Boolean("Permission To Treat")
    blood_type = fields.Char("Blood Type")

    # Academic
    enrollment_history_ids = fields.One2many('school.enrollment.history', 'student_id', copy=True)

    program_ids = fields.Many2many('school.program', store=True, compute='_compute_academics')
    school_ids = fields.Many2many('school.school', store=True, compute='_compute_academics')
    grade_level_ids = fields.Many2many(
        'school.grade.level', string="Grade Levels", store=True, compute='_compute_academics')
    district_ids = fields.Many2many('school.district', compute='_compute_academics', store=True)
    enrollment_status_ids = fields.Many2many(
        'school.enrollment.status', string="Enrollment status", store=True, compute='_compute_academics')

    # wizard related resource field
    wizard_student_id = fields.Integer()
    reference_id = fields.Char('Student Reference ID')

    # == Academics fields ==
    enrollment_state_ids = fields.One2many('school.student.enrollment.state', 'student_id', string="Enroll states")
    relationship_ids = fields.One2many('school.student.relationship', 'student_id', string="Relationships")
    homeroom = fields.Char(string="Homeroom")

    # discount tab

    concession_line_ids     =   fields.One2many('consession.line', 'student_id', string="Concession Line")




    ##############################
    # Compute and search methods #
    ##############################
    @api.depends(
        'enrollment_state_ids',
        'enrollment_state_ids.grade_level_id',
        'enrollment_state_ids.program_id',
        'enrollment_state_ids.enrollment_status_id',
        'enrollment_state_ids.enrollment_sub_status_id',
        )
    def _compute_academics(self):
        for student in self:
            enrollment_histories = student.enrollment_state_ids
            student.grade_level_ids = enrollment_histories.mapped('grade_level_id')
            student.program_ids = enrollment_histories.mapped('program_id')
            student.school_ids = student.program_ids.mapped('school_id')
            student.district_ids = student.school_ids.mapped('district_id')
            student.enrollment_status_ids = enrollment_histories.mapped('enrollment_status_id')

    def is_in_allowed_program(self):
        self.ensure_one()
        allowed_programs = self.env.programs.get_with_parent()
        return bool([p_id for p_id in self.program_ids if p_id in allowed_programs])

    ############################
    # Constrains and onchange  #
    ############################
    @api.onchange("first_name", "middle_name", "last_name")
    def onchange_student_name(self):
        self.name = self.individual_id.format_name(self.first_name, self.middle_name, self.last_name)

    #########################
    # CRUD method overrides #
    #########################
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if not self.env.su and not self._context.get('no_program_filter', False):
            allowed_programs = self.env.programs.get_with_parent()
            program_domain = [('program_ids', 'in', allowed_programs.ids)]
            search_domain = expression.AND([program_domain, args])
        else:
            search_domain = args
        return super(SchoolStudent, self)._search(search_domain, offset, limit, order, count, access_rights_uid)

    @api.model
    def _read_group_raw(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if not self.env.su and not self._context.get('no_program_filter', False):
            allowed_programs = self.env.programs.get_with_parent()
            program_domain = [('program_ids', 'in', allowed_programs.ids)]
            search_domain = expression.AND([program_domain, domain])
        else:
            search_domain = domain
        res = super()._read_group_raw(search_domain, fields, groupby, offset, limit, orderby, lazy)
        return res

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
    def open_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'name': self.partner_name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            }

    def get_enroll_status_line(self, program_id: int):
        self.ensure_one()
        return self.enrollment_state_ids.filtered(lambda es: es.program_id.id == program_id)

#school.structure.district

class SchoolBaseDistrict(models.Model):
    """ Districts """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.district'
    _description = "District"
    _order = "sequence"
    _rec_name = 'display_name'
    _inherit = ['school.mixin.with.code', 'image.mixin']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    sequence = fields.Integer(default=1)
    school_ids = fields.One2many(
        "school.school", "district_id", string="School")
    company_ids = fields.Many2many(
        "res.company", string="Companies",
        default=lambda self: self.env.companies,
        relation='district_company_rel', column1='district_id', column2='company_id', required=True)
    reference_id = fields.Char('District Reference ID')

#school.structure.grade.level

class SchoolBaseGradeLevel(models.Model):
    """ Grade levels """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.grade.level'
    _order = "sequence"
    _description = "Grade level"
    _rec_name = 'display_name'
    _inherit = ['school.mixin.with.code', 'image.mixin']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=1)
    program_id = fields.Many2one('school.program')
    school_id = fields.Many2one('school.school', related='program_id.school_id', store=True)
    district_id = fields.Many2one(related="school_id.district_id", store=True)
    capacity = fields.Integer()
    reference_id = fields.Char('Grade Level Reference ID')
    next_program_id = fields.Many2one('school.program', string="Next Program")
    next_grade_level_id = fields.Many2one('school.grade.level', string="Next Grade Level", domain="[('program_id', '=', next_program_id)]")
    next_status_id = fields.Many2one('school.enrollment.status', string="Next Status")

#school.structure.period

class PeriodCategory(models.Model):
    """ Period category """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.period.category'
    _description = "School period category"
    _rec_name = 'display_name'

    name = fields.Char()
    display_name = fields.Char(compute='_compute_recursive_name', store=True)

    # key = fields.Char()
    # todo: David multiple keys

    parent_id = fields.Many2one('school.period.category')
    child_ids = fields.One2many('school.period.category', 'parent_id')
    reference_id = fields.Char()

    @api.depends('parent_id.name', 'name')
    def _compute_recursive_name(self):
        for period in self:
            period.display_name = period._get_recursive_parent_name()

    def _get_recursive_parent_name(self):
        self.ensure_one()
        name = self.name
        if self.parent_id:
            name = "%s / %s" % (self.parent_id._get_recursive_parent_name(), name)
        return name


class Period(models.Model):
    """ Period """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.period'
    _description = "School period"
    _order = 'date_start desc'
    _inherit = ['school.mixin.with.code', 'image.mixin']

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    name = fields.Char(translate=True)
    parent_name = fields.Char(compute='compute_parent_full_name', store=True)

    category_id = fields.Many2one('school.period.category', required=True)

    program_id = fields.Many2one(
        'school.program', store=True,
        required=True, readonly=False, compute='compute_program_id',
        recursive=True)
    # class_ids = fields.Many2many(
    #     'school.class', relation='class_period_rel',
    #     column1='period_id', column2='class_id')

    parent_id = fields.Many2one('school.period')
    child_ids = fields.One2many('school.period', 'parent_id')

    date_start = fields.Date(
        compute='compute_dates', store=True, readonly=False, recursive=True)
    date_end = fields.Date(
        compute='compute_dates', store=True, readonly=False, recursive=True)
    reference_id = fields.Char('Period Reference ID')

    @api.depends('parent_id', 'parent_id.display_name')
    def compute_parent_full_name(self):
        for period in self:
            if period.parent_id:
                period.parent_name = period.parent_id._get_recursive_parent_name()
            else:
                period.parent_name = period._get_recursive_parent_name()

    @api.depends('child_ids', 'child_ids.date_start', 'child_ids.date_end')
    def compute_dates(self):
        for period in self:
            if period.child_ids:
                first_child = period.child_ids.filtered(lambda x: x.date_start).sorted('date_start')
                last_child = period.child_ids.filtered(lambda x: x.date_start).sorted('date_start', reverse=True)

                period.date_start = first_child[0].date_start if first_child else False
                period.date_end = last_child[0].date_end if last_child else False
            else:
                period.date_start = False
                period.date_end = False

    # @api.constrains('date_start', 'date_end')
    # def _check_date_collision_constraint(self):
    #    """ Check that date doesn't collide with other sibling period """
    #    for period in self:
    #        sibling_periods = period.parent_id.child_ids - period
    #        for s_period in sibling_periods:
    #            period._check_collision(s_period)

    def _check_collision(self, other_period):
        """ We are going to use AABB collision inspiration"""
        self.ensure_one()
        other_period.ensure_one()
        if self.date_end >= other_period.date_start and self.date_start <= other_period.date_end:
            raise UserError(_("Date collision between %s and %s\n"
                              "Date range of %s (%s)-(%s)\n"
                              "Date range of %s (%s)-(%s)") % (
                                self.name, other_period.name,
                                self.name, self.date_start, self.date_end,
                                other_period.name, other_period.date_start,
                                other_period.date_end))

    def _get_period_recursive_parent_name(self):
        self.ensure_one()
        name = "%s / %s / %s / %s" % (self.program_id.school_id.district_id.name,
                                      self.program_id.school_id.name, self.program_id.name, self.name)
        if self.parent_id:
            name = " %s / %s" % (self.parent_id._get_period_recursive_parent_name(), name)

        return name

    def _compute_display_name(self):
        for period in self:
            period.display_name = period._get_period_recursive_parent_name()

    def _get_recursive_parent_name(self):
        self.ensure_one()
        name = self.name
        if self.parent_id:
            name = "%s / %s" % (self.parent_id._get_recursive_parent_name(), name)
        return name

    @api.model
    def display_name_depends(self):
        return ['code',
                'name',
                'parent_id',
                'parent_id.name',
                'parent_id.code',
                'parent_id.display_name']

    @api.depends(lambda self: self.display_name_depends())
    def compute_name(self):
        for record in self:
            record.display_name = record._get_recursive_parent_name()

    ##################
    # Compute method #
    ##################

    @api.depends('parent_id', 'parent_id.program_id')
    def compute_program_id(self):
        for period in self:
            if period.parent_id:
                period.program_id = period.parent_id.program_id
            else:
                period.program_id = False


#school.structure.program

class Program(models.Model):
    """ Program """
    ######################
    # Private Attributes #
    ######################
    _name = 'school.program'
    _description = "School program"
    _inherit = ['school.mixin.with.code']
    _rec_name = 'name'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    full_path_name = fields.Char('Full path name', compute='_compute_full_path_name')
    school_id = fields.Many2one('school.school', group_expand='_expand_schools', required=True)
    school_district_id = fields.Many2one('school.district', related='school_id.district_id', store=True)

    period_ids = fields.One2many('school.period', 'program_id')

    grade_level_ids = fields.One2many('school.grade.level', 'program_id')
    parent_id = fields.Many2one('school.program')
    child_ids = fields.One2many('school.program', 'parent_id')
    reference_id = fields.Char('Program Reference ID')

    ##################
    # Compute method #
    ##################
    def _expand_schools(self, states, domain, order):
        company_ids = self.env.companies
        return company_ids.district_ids.school_ids

    def get_with_parent(self):
        programs = self
        for program in self:
            if program.parent_id:
                parent_programs = program.parent_id.get_with_parent()
                for parent_program in parent_programs:
                    if parent_program not in programs:
                        programs += parent_programs
        return programs

    def _get_program_recursive_parent_name(self):
        self.ensure_one()
        name = "%s / %s / %s" % (self.school_id.district_id.name, self.school_id.name, self.name)
        if self.parent_id:
            name = "%s / %s" % (self.parent_id._get_program_recursive_parent_name(), name)

        return name

    def _compute_full_path_name(self):
        for program in self:
            program.full_path_name = program._get_program_recursive_parent_name()
    #########################
    # CRUD method overrides #
    #########################
    @api.model
    def create(self, vals):
        res = super().create(vals)
        user_write_vals = {'user_program_ids': [Command.link(res.id)]}
        if not self.env.user.user_program_id:
            user_write_vals['user_program_id'] = res.id
        self.env.user.write(user_write_vals)
        return res

#school.structure.school

class SchoolBaseSchool(models.Model):
    """ Schools """

    ######################
    # Private Attributes #
    ######################
    _name = 'school.school'
    _description = "School"
    _order = "sequence"
    _inherit = ['school.mixin.with.code', 'image.mixin']
    _rec_name = 'display_name'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    description = fields.Char("Description")
    sequence = fields.Integer(default=1)
    district_id = fields.Many2one(
        "school.district", "District", required=True, group_expand='_expand_districts')
    program_ids = fields.One2many("school.program", 'school_id')

    district_company_ids = fields.Many2many(
        'res.company', related='district_id.company_ids', string="District companies")
    company_ids = fields.Many2many(
        'res.company', string="Companies",
        relation='school_company_rel', column1='school_id', column2='company_id',
        required=True,
        store=True,
        readonly=False,
        compute='compute_company_ids'
        )
    reference_id = fields.Char('School Reference ID')

    ##############################
    # Compute and search methods #
    ##############################
    def _expand_districts(self, states, domain, order):
        return self.env.companies.district_ids

    @api.depends('district_id', 'district_company_ids')
    def compute_company_ids(self):
        for school in self:
            # We check if the school has some company that isn't in the district's companies
            if not school.company_ids:
                school.company_ids = school.district_company_ids
            elif not all(school.company_ids.mapped(lambda c: c in self.district_company_ids)):
                # We need to remove that company
                companies = school.company_ids.filtered(lambda c: c in self.district_company_ids)
                if not companies:
                    # It is possible that the district code removed all the school companies
                    companies = school.district_company_ids
                school.company_ids = companies

#technical.re.enrollment.record

class SchoolBaseReenrollmentRecord(models.Model):
    _name = 'school.reenrollment.record'
    _description = "Reenrollment record"
    _order = 'create_date desc'

    period_id = fields.Many2one('school.period', required=True)
    # school_year_start_date
    next_grade_level_id = fields.Many2one('school.grade.level')
    reenrollment_status = fields.Selection([
                ("open", "Open"),
                ("finished", "Finished"),
                ("withdrawn", "Withdrawn"),
                ("rejected", "Rejected"),
                ("blocked", "Blocked"),
            ], string="Reenrollment Status")
    partner_id = fields.Many2one('res.partner', required=True)
    note = fields.Text()


