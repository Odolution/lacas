# -*- coding: utf-8 -*-
from lxml import etree

from odoo import models, fields, api, _
from odoo.fields import Command
import logging

logger = logging.getLogger(__name__)

# enroll.student.form

def isInt(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


class EnrollStudentForm(models.TransientModel):
    """ Enrollment Students Form """
    _name = 'enroll.student.form'
    _description = ' Enrollment Students Form '

    name = fields.Char("Name")

    # If you ask why aren't they just 1,2,3,4.
    # This is because this is supposed to be extended by any module and put its custom steps
    state = fields.Selection(
        selection=[
            ("0", "Students"),
            ("10", "Family"),
            ("20", "Relationship"),
            ('done', "Done"),
            ], default="0")

    student_ids = fields.One2many('enroll.student.form.student', 'form_id')
    individual_ids = fields.Many2many(
        'enroll.student.form.individual', store=False, compute='compute_individual_ids',
    )

    @api.depends('family_ids', 'family_ids.individual_ids')
    def compute_individual_ids(self):
        for form in self:
            form.individual_ids = form.mapped('family_ids.individual_ids')

    # Step 2
    family_ids = fields.One2many('enroll.student.form.family', 'form_id')
    real_family_ids = fields.Many2many('school.family', store=False, compute='compute_real_family_ids')

    # Step 3 - Relationships
    relationship_ids = fields.One2many('enroll.student.form.relationship', 'form_id', string="Relationships")

    def move_previous_step(self):
        self.ensure_one()
        prev_state = self.state
        form_states = self.get_sorted_form_states()
        if self.state != str(form_states[0]) and self.state != 'done':
            index = form_states.index(int(self.state))
            self.state = str(form_states[index - 1])
        elif self.state == 'done':
            self.state = str(form_states[-2])
        new_state = self.state
        self.on_move_step(prev_state, new_state)

    def move_next_step(self):
        self.ensure_one()
        prev_state = self.state
        if self.state != 'done' and isInt(self.state):
            form_states = self.get_sorted_form_states()
            index = form_states.index(int(self.state))
            self.state = str(form_states[index + 1])
        new_state = self.state
        self.on_move_step(prev_state, new_state)

    def on_move_step(self, prev_state, new_state):
        on_move_step_method_name = f'on_move_step_{new_state}'
        if hasattr(self, on_move_step_method_name):
            on_move_step_method = getattr(self, on_move_step_method_name)
            on_move_step_method(prev_state, new_state)

    def on_move_step_20(self, prev_state, new_state):
        self.recompute_relationships()

    def recompute_relationships(self):
        self.ensure_one()

        new_relationship_values = []
        student_individual_relations = []
        for family in self.family_ids:
            for student in family.student_ids:
                for individual in family.individual_ids:
                    if not any(filter(lambda vals: vals['student'] == student and vals['individual'] == individual, student_individual_relations)):
                        student_individual_relations.append({
                            'individual': individual,
                            'student': student,
                            })

        def should_be_added(_student, _individual):
            for _relationship in self.relationship_ids:
                if _relationship.student_id == _student and _relationship.individual_id == _individual:
                    return False
            return True

        def should_be_removed(_student, _individual):
            for _relation in student_individual_relations:
                if _relation['student'] == _student and _relation['individual'] == _individual:
                    return False
            return True

        for relation in student_individual_relations:
            student = relation['student']
            individual = relation['individual']
            if should_be_added(student, individual):
                new_relationship_values.append(Command.create({
                        'individual_id': individual.id,
                        'student_id': student.id,
                        'relationship_id': individual.default_relationship_id.id,
                    }))

        for relationship in self.relationship_ids:
            student = relationship.student_id
            individual = relationship.individual_id
            if should_be_removed(student, individual):
                new_relationship_values.append(Command.delete(relationship.id))

        self.update({'relationship_ids': new_relationship_values})

    def enroll(self):
        self._create_families()

        self._create_individuals()
        students = self._create_students()
        self._create_relationships()

        self._student_created()
        action = self.action_view_students(students)

        self.unlink()
        return action

    def _create_families(self):
        families = self.env['school.family']
        for form_family in self.family_ids:
            if not form_family.real_family_id:
                values = form_family.prepare_values()
                real_family = families.create(values)
                form_family.real_family_id = real_family
            families += form_family.real_family_id
        return families

    def _create_individuals(self):
        individuals = self.env['school.family.individual']
        for form_individual in self.mapped('family_ids.individual_ids'):
            values = form_individual.prepare_values()
            if not form_individual.real_individual_id:
                real_individual = individuals.create(values)
                form_individual.real_individual_id = real_individual
            else:
                form_individual.real_individual_id.write(values)
            individuals += form_individual.real_individual_id
        return individuals

    def _create_students(self):
        students = self.env['school.student']
        for form_student in self.student_ids:
            if not form_student.real_student_id:
                values = form_student.prepare_values()
                real_student = students.create(values)
                form_student.real_student_id = real_student
            students += form_student.real_student_id
        return students

    def _create_relationships(self):
        relationships = self.env['school.student.relationship']
        for form_relationship in self.relationship_ids:
            values = form_relationship.prepare_values()
            real_relationship = relationships.create(values)
            relationships += real_relationship
        return relationships

    def _student_created(self):
        """ Method to be inherited by any module if needed (e.g: ol_school_manager_finance) """
        pass

    @api.model
    def get_sorted_form_states(self):
        form_states_unfiltered = dict(self._fields['state']._description_selection(self.env)).keys()
        form_states = [int(state) for state in form_states_unfiltered if isInt(state)]
        form_states = sorted(form_states)
        form_states.append('done')
        return form_states

    @api.model
    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super()._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            form_states = [str(state) for state in self.get_sorted_form_states()]
            form_states.remove('done')
            doc = etree.XML(result['arch'])
            statebar = doc.xpath("//form//field[@name='state']")
            first_step = form_states[0]
            last_step = form_states[-1]

            if statebar:
                statusbar_visible = ",".join(form_states)
                statebar[0].attrib['statusbar_visible'] = statusbar_visible

            step_groups = doc.xpath("//form//group[@ol_school_manager_step]")
            for group in step_groups:
                ol_school_manager_step = group.attrib['ol_school_manager_step']
                group.attrib['attrs'] = f"{{'invisible': [('state', '!=', '{ol_school_manager_step}')]}}"

            button_move_previous_step = doc.xpath("//form//button[@name='move_previous_step']")
            if button_move_previous_step:
                button_move_previous_step[0].attrib['attrs'] = f"{{'invisible': [('state', '=', '{first_step}')]}}"

            button_move_next_step = doc.xpath("//form//button[@name='move_next_step']")
            if button_move_next_step:
                button_move_next_step[0].attrib['attrs'] = f"{{'invisible': [('state', '=', '{last_step}')]}}"

            button_enroll = doc.xpath("//form//button[@name='enroll']")
            if button_enroll:
                button_enroll[0].attrib['attrs'] = f"{{'invisible': [('state', '!=', '{last_step}')]}}"
            result['arch'] = etree.tostring(doc, encoding='unicode')
        return result

    @api.depends('family_ids', 'family_ids.real_family_id')
    def compute_real_family_ids(self):
        for form in self:
            form.real_family_ids = form.mapped('family_ids.real_family_id')

    def new_virtual_family(self):
        family = self.env['enroll.student.form.family'].create({})
        family.onchange_individual_ids()
        return family.id

    def get_default_individuals_values(self):
        self.ensure_one()
        individuals_values = []
        default_last_name = self.get_default_last_name()
        for i in range(1, 3):
            values = {
                'first_name': _("Individual %s", i),
                'last_name': default_last_name,
                'form_id': self.id,
                }
            individuals_values.append(values)
        return individuals_values

    def get_default_last_name(self):
        return self.student_ids[:1].last_name

    @api.model
    def action_view_students(self, students):
        action = self.env["ir.actions.actions"]._for_xml_id("ol_school_manager.action_school_students")
        if len(students) > 1:
            action['domain'] = [('id', 'in', students.ids)]
        elif len(students) == 1:
            form_view = [(self.env.ref('ol_school_manager.school_student_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = students.id
        else:
            action = {
                'type': 'ir.actions.act_window_close'
                }
        action['target'] = 'main'
        return action

# family

class EnrollStudentFormFamily(models.TransientModel):
    _name = 'enroll.student.form.family'
    _description = "School enroll form family"

    @api.model
    def default_get(self, fields_list):
        context = self._context
        res = super().default_get(fields_list)

        form_id = context.get('default_form_id', False)

        form = self.env['enroll.student.form'].browse(form_id)
        if form and 'student_ids' in fields_list and not res.get('student_ids'):
            res['student_ids'] = [Command.set(form.student_ids.ids)]

        if context.get('real_family_id', False):
            FormFamilyEnv = self.env['school.family'].sudo()
            existing_family = FormFamilyEnv.browse(context['real_family_id'])
            existing_family_values = existing_family.prepare_enroll_form_family_default_values()
            res.update(existing_family_values)
        elif form:
            individuals_values = form.get_default_individuals_values()
            individuals = self.env['enroll.student.form.individual'].sudo().create(individuals_values)
            individuals._compute_name()
            res['individual_ids'] = [Command.set(individuals.ids)]
        return res

    form_id = fields.Many2one('enroll.student.form', required=True, ondelete='cascade', default=12)
    real_family_id = fields.Many2one('school.family')
    name = fields.Char(required=True, default='New family')

    form_student_ids = fields.Many2many('enroll.student.form.student', string="Form students", compute='compute_form_student_ids')
    student_ids = fields.Many2many(
        'enroll.student.form.student', domain="[('id', 'in', form_student_ids)]",
        relation='enroll_student_form_student_family_rel',
        column1='family_id',
        column2='student_id',
        )
    individual_ids = fields.Many2many(
        'enroll.student.form.individual',
        relation='enroll_student_form_student_individual_rel',
        column1='family_id',
        column2='individual_id',
        domain="[('id', 'not in', real_individual_ids)]",
        )
    individual_names = fields.Char(compute='_compute_individual_names')
    real_individual_ids = fields.Many2many('school.family.individual', store=False, compute='compute_real_individual_ids')
    individual_in_form_ids = fields.Many2many('enroll.student.form.individual', store=False, related='form_id.individual_ids')
    real_individual_in_form_ids = fields.Many2many('school.family.individual', store=False, compute='compute_real_individual_in_form_ids')

    @api.depends('individual_ids', 'individual_ids.real_individual_id')
    def compute_real_individual_ids(self):
        for form in self:
            form.real_individual_ids = form.mapped('individual_ids.real_individual_id')

    @api.depends('form_id', 'form_id.student_ids')
    def compute_form_student_ids(self):
        for family in self:
            family.form_student_ids = family.mapped('form_id.student_ids')

    @api.depends('form_id', 'individual_in_form_ids', 'form_id.individual_ids', 'form_id.individual_ids.real_individual_id')
    def compute_real_individual_in_form_ids(self):
        for family in self:
            family.real_individual_in_form_ids = family.mapped('individual_in_form_ids.real_individual_id')

    @api.onchange('form_id', 'individual_ids')
    def onchange_individual_ids(self):
        default_family_name = self._get_default_family_name()
        self.name = default_family_name

    def _get_default_family_name(self):
        self.ensure_one()
        individual1 = self.individual_ids[:1]
        individual1._compute_name()
        individual2 = self.individual_ids[1:2]
        individual2._compute_name()
        if individual1 and individual2:
            if individual1.last_name == individual2.last_name:
                return _("Family of %s, %s and %s", individual1.last_name, individual1.first_name, individual2.first_name)
            return _("Family of %s, %s and %s, %s", individual1.last_name, individual1.first_name, individual2.last_name, individual2.first_name)
        elif individual1:
            return _("Family of %s", individual1.name)
        return _("New Family")

    @api.depends('individual_ids.name', 'individual_ids.first_name', 'individual_ids.middle_name', 'individual_ids.last_name')
    def _compute_individual_names(self):
        for family in self:
            self.individual_names = ','.join([individual.name for individual in family.individual_ids])

    def prepare_values(self):
        self.ensure_one()
        return {
            'name': self.name,
            }

# individual

class EnrollStudentFormIndividual(models.TransientModel):
    _name = 'enroll.student.form.individual'
    _description = "Enroll student form: individual"
    _inherit = 'image.mixin'
    _rec_name = 'name'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        form_id = self._context.get('default_form_id', False)
        if 'form_id' in fields_list and not res.get('form_id'):
            res['form_id'] = form_id

        if form_id:
            form = self.env['enroll.student.form'].browse(form_id)
            res['last_name'] = form.get_default_last_name()

        return res

    name = fields.Char(compute="_compute_name", store=False)

    first_name = fields.Char(required=True)
    middle_name = fields.Char()
    last_name = fields.Char(required=True)

    # Demographics
    date_of_birth = fields.Date(string="Date of birth")
    gender = fields.Many2one('school.gender', string="Gender")
    citizenship = fields.Char(string='Citizenship')
    ethnicity = fields.Char(string='Ethnicity')
    race = fields.Char(string='Race')

    phone = fields.Char()
    mobile = fields.Char()
    email = fields.Char()
    email2 = fields.Char()
    form_id = fields.Many2one('enroll.student.form', required=True, ondelete='cascade')

    # Address
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    family_ids = fields.Many2many(
        'enroll.student.form.family',
        relation='enroll_student_form_student_individual_rel',
        column1='individual_id',
        column2='family_id',
        )
    default_relationship_id = fields.Many2one(
        'school.student.relationship.type', ondelete='cascade',
        default=lambda self: self.env['school.student.relationship.type'].get_default_parent_relationship()
        )
    real_individual_id = fields.Many2one('school.family.individual', string="Real individual")

    @api.onchange('first_name', 'middle_name', 'last_name')
    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        for student in self:
            student.name = self.env['school.family.individual'].format_name(student.first_name, student.middle_name, student.last_name)

    def prepare_values(self):
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
            'family_ids': [Command.link(family.id) for family in self.mapped('family_ids.real_family_id')],
            }


class EnrollStudentFormFamilyRelationships(models.TransientModel):
    _name = 'enroll.student.form.relationship'
    _description = "Enroll student form: relationship"
    _order = 'student_id, individual_id'

    form_id = fields.Many2one('enroll.student.form', required=True, ondelete='cascade')
    student_id = fields.Many2one('enroll.student.form.student', required=True, ondelete='cascade')
    individual_id = fields.Many2one('enroll.student.form.individual', required=True, ondelete='cascade')
    relationship_id = fields.Many2one('school.student.relationship.type', required=True, ondelete='cascade')

    def prepare_values(self):
        self.ensure_one()
        return {
            'student_id': self.student_id.real_student_id.id,
            'individual_id': self.individual_id.real_individual_id.id,
            'relationship_type_id': self.relationship_id.id,
            }

# sudent.enrollment.state

class EnrollStudentFormStudentEnrollmentState(models.TransientModel):
    _name = 'enroll.student.form.student.enrollment.state'
    _description = 'Student enrollment state for enroll form'

    student_id = fields.Many2one('enroll.student.form.student')

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

    enrolled_date = fields.Date(string="Enrolled date", default=fields.Date.today())
    graduation_date = fields.Date(string="Graduation date")
    withdraw_date = fields.Date(string="Withdraw date")
    note = fields.Text(string="Note")

    _sql_constraints = [
        ('student_program_unique',
         'unique(student_id, program_id)',
         "You cannot have more than one enrollment state for the same student in the same program"),
        ]

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

    def prepare_values(self):
        self.ensure_one()
        return {
            'student_id': self.student_id.real_student_id.id,
            'program_id': self.program_id.id,
            'school_id': self.school_id.id,
            'grade_level_id': self.grade_level_id.id,
            'enrollment_status_id': self.enrollment_status_id.id,
            'enrollment_sub_status_id': self.enrollment_sub_status_id.id,
            'next_program_id': self.next_program_id.id,
            'next_school_id': self.next_school_id.id,
            'next_grade_level_id': self.next_grade_level_id.id,
            'next_enrollment_status_id': self.next_enrollment_status_id.id,
            'next_enrollment_sub_status_id': self.next_enrollment_sub_status_id.id,
            'enrolled_date': self.enrolled_date,
            'graduation_date': self.graduation_date,
            'withdraw_date': self.withdraw_date,
            'note': self.note,
            }

# student

class EnrollStudentFormStudent(models.TransientModel):
    _name = 'enroll.student.form.student'
    _description = 'Enroll student form student'
    _inherit = 'enroll.student.form.individual'

    enrollment_state_ids = fields.One2many('enroll.student.form.student.enrollment.state', 'student_id')
    family_ids = fields.Many2many(
        'enroll.student.form.family',
        relation='enroll_student_form_student_family_rel',
        column1='student_id',
        column2='family_id',
        )
    real_student_id = fields.Many2one('school.student', string="Real student")

    def prepare_values(self):
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
            'family_ids': [Command.set(self.mapped('family_ids.real_family_id').ids)],
            'enrollment_state_ids': [Command.create(enroll_state.prepare_values()) for enroll_state in self.enrollment_state_ids],
            }