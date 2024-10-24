# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError
import logging
from odoo.fields import Command
import json
from odoo.tools.safe_eval import safe_eval, test_python_expr

_logger = logging.getLogger(__name__)


class OlMigrationToolWizard(models.TransientModel):
    _name = 'ol.migration.tool.wizard'
    _description = ' Migration Tool Wizard'

    name = fields.Char()
    student = fields.Integer(string='Students', compute='_compute_resume_record')
    families = fields.Integer(string='Families', compute='_compute_resume_record')
    individuals = fields.Integer(string='Individuals', compute='_compute_resume_record')
    districts = fields.Integer(string='Districts', compute='_compute_resume_record')
    schools = fields.Integer(string='Schools', compute='_compute_resume_record')
    programs = fields.Integer(string='Programs', compute='_compute_resume_record')
    period_categories = fields.Integer(string='Period Categories', compute='_compute_resume_record')
    periods = fields.Integer(string='Periods', compute='_compute_resume_record')
    grade_level = fields.Integer(string='Grade Level', compute='_compute_resume_record')
    select_method = fields.Selection([('custom', "Custom Method"), ('import', "Import Excel")], required=True)
    custom_method = fields.Many2one('ol.migration.tool.method', string="Custom Method")
    generated_json = fields.Text(string="Generated JSON")

    @api.model
    def _search_reference_id_in_ol_dict(self, reference: str, record_dict: dict):
        if isinstance(record_dict, dict):
            for k, v in record_dict.items():
                if k == 'id' and v == reference:
                    return record_dict
                else:
                    returned_record_dict = self._search_reference_id_in_ol_dict(reference, v)
                    if returned_record_dict:
                       return returned_record_dict
        elif isinstance(record_dict, list):
            for item in record_dict:
                returned_record_dict = self._search_reference_id_in_ol_dict(reference, item)
                if returned_record_dict:
                   return returned_record_dict

    def generate_json(self):
        self.ensure_one()
        self.generated_json = self.custom_method.generate_json()

    def button_generate_json(self):
        self.ensure_one()
        self.generate_json()
        if not self.generated_json:
            raise UserError(_("JSON cannot be empty!"))
        ol_dict = json.loads(self.generated_json)
        self.create_ol_records(ol_dict)

    def create_ol_records(self, ol_dict):
        self.create_school_structure_records(ol_dict)
        self.create_people_records(ol_dict)

    def create_school_structure_records(self, ol_dict):
        self.create_districts(ol_dict)
        self.create_schools(ol_dict)
        self.create_programs(ol_dict)
        self.create_period_categories(ol_dict)
        self.create_periods(ol_dict)
        self.create_grade_levels(ol_dict)

    def create_people_records(self, ol_dict):
        self.create_families(ol_dict)
        self.create_students(ol_dict)
        self.create_individuals(ol_dict)
        self.update_relationships(ol_dict)
        self.update_student_relationship(ol_dict)

    def create_districts(self, ol_dict):
        districts = self.env['school.district']
        if "districts" not in ol_dict:
            raise ValidationError(_("You should add districts in the JSON structure"))
        for district in ol_dict["districts"]:
            district_values = self._extract_district(district, ol_dict)
            real_district = self.env['school.district'].create(district_values)
            districts += real_district
            district["real_record"] = real_district
        return districts

    def create_schools(self, ol_dict):
        schools = self.env['school.school']
        if "schools" not in ol_dict:
            raise ValidationError(_("You should add schools in the JSON structure"))
        for school_values in ol_dict["schools"]:
            school = self._create_ol_record_from_values(ol_dict, school_values, 'school.school')
            schools += school
        return schools

    def create_programs(self, ol_dict):
        programs = self.env['school.program']
        if "programs" not in ol_dict:
            raise ValidationError(_("You should add programs in the JSON structure"))
        for program_values in ol_dict["programs"]:
            program = self._create_ol_record_from_values(ol_dict, program_values, 'school.program')
            programs += program
        return programs

    def create_period_categories(self, ol_dict):
        period_categories = self.env['school.period.category']
        if "period_categories" in ol_dict:
            for period_category_values in ol_dict["period_categories"]:
                period_category = self._create_ol_record_from_values(ol_dict, period_category_values, 'school.period.category')
                period_categories += period_category
        return period_categories

    def create_periods(self, ol_dict):
        periods = self.env['school.period']
        if "periods" in ol_dict:
            for period_values in ol_dict["periods"]:
                period = self._create_ol_record_from_values(ol_dict, period_values, 'school.period')
                periods += period
        return periods

    def create_grade_levels(self, ol_dict):
        grade_levels = self.env['school.grade.level']
        if "grade_levels" not in ol_dict:
            raise ValidationError(_("You should add grade levels in the JSON structure"))
        for grade_level_values in ol_dict["grade_levels"]:
            grade_level = self._create_ol_record_from_values(ol_dict, grade_level_values, 'school.grade.level')
            grade_levels += grade_level
        return grade_levels

    def create_families(self, ol_dict):
        families = self.env['school.family']
        if "families" not in ol_dict:
            raise ValidationError(_("You should add Family in the JSON structure"))
        for family in ol_dict["families"]:
            family_values = self._extract_families(family, ol_dict)
            real_family = self.env['school.family'].create(family_values)
            families += real_family
            family["real_record"] = real_family
        return families

    def create_students(self, ol_dict):
        students = self.env['school.student']
        if "students" not in ol_dict:
            raise ValidationError(_("You should add students in the JSON structure"))
        for student in ol_dict["students"]:
            student_values = self._extract_students(student, ol_dict)
            real_student = self.env['school.student'].create(student_values)
            students += real_student
            student["real_record"] = real_student
        return students

    def create_individuals(self, ol_dict):
        individuals = self.env['school.family.individual']
        if "individuals" not in ol_dict:
            raise ValidationError(_("You should add Individuals in the JSON structure"))
        for individual in ol_dict["individuals"]:
            individual_values = self._extract_individuals(individual, ol_dict)
            real_individual = self.env['school.family.individual'].create(individual_values)
            individuals += real_individual
            individual["real_record"] = real_individual
        return individuals

    def update_relationships(self, ol_dict):
        for family in ol_dict['families']:
            family_real_record = family['real_record']
            family_values = self._get_family_relation_values(family, ol_dict, family_real_record)
            family_real_record.write(family_values)

    def update_student_relationship(self, ol_dict):
        for student in ol_dict['students']:
            student_real_record = student['real_record']
            student_values = self._get_student_relation_values(student, ol_dict, student_real_record)
            student_real_record.write(student_values)

    @api.model
    def _get_real_record(self, reference_id, model, ol_key, ol_dict):
        _logger.info(f"{reference_id}, {model}, {ol_key}")
        if type(reference_id) == str:
            # It is an external id or a reference in the JSON dict
            if ol_key not in ol_dict:
                return self.env.ref(reference_id, raise_if_not_found=False) or False
            else:
                ol_value = ol_dict[ol_key]
                for value in ol_value:
                    if type(value) == dict and value['id'] == reference_id:
                        return value['real_record']
        elif type(reference_id) == int:
            # Then it may be an id for X model
            record = self.env[model].browse(reference_id)
            if record.exists():
                return record

    @api.model
    def _format_as_many2one(self, ol_dict, comodel, value_to_format):
        if type(value_to_format) == int:
            # We do this to filter the existence of the id
            return self.env[comodel].browse(value_to_format)
        elif type(value_to_format) == str:
            record_dict = self._search_reference_id_in_ol_dict(
                value_to_format, ol_dict)
            if not record_dict or 'real_record' not in record_dict:
                return self.env.ref(value_to_format,
                                    raise_if_not_found=False) or self.env[
                           comodel]
            else:
                return record_dict['real_record']
        raise ValidationError(_("Wrong format of many2one field"))

    @api.model
    def _format_field_value(self, model: str, field_key: str, value, ol_dict: dict):
        field = self.env[model]._fields.get(field_key, False)

        if not field or field_key == 'id':
            return False
        if field.type == 'many2one':
            try:
                return self._format_as_many2one(ol_dict, field.comodel_name, value).id
            except ValidationError:
                return False
        elif field.type in ('many2many', 'many2one'):
            if type(value) != list:
                raise ValidationError(_("Wrong format for x2many field: %s", field_key))
            command_list = []
            for element in value:
                if type(element) == dict:
                    element_values = self._get_formatted_record_values(ol_dict, element, field.comodel_name)
                    command_list.append(Command.create(element_values))
                else:
                    command_list.append(Command.link(self._format_as_many2one(ol_dict, field.comodel_name, element).id))
            return command_list
        elif field.type in ('char', 'text', 'html', 'selection'):
            return str(value)
        elif field.type == 'integer':
            return int(value)
        elif field.type in ('float', 'monetary'):
            return float(value)
        elif field.type == 'date':
            return fields.Date.from_string(value)
        elif field.type == 'datetime':
            return fields.Datetime.from_string(value)
        elif field.type == 'boolean':
            return bool(value)

        raise ValidationError(_("Unsupported the field type (%s) of: %s, model: %s", field_key, field.type, ))

    @api.model
    def _extract_district(self, district, ol_dict):
        district = dict(district)
        company_ids = district.get('company_ids', [])
        if not company_ids or type(company_ids) != list:
            raise ValidationError(_("company_ids field's value in districts is not valid"))
        district_values = self._get_formatted_record_values(ol_dict, district, 'school.district')
        return district_values

    def _create_ol_record_from_values(self, ol_dict: dict, values: dict, model: str):
        record_values = self._extract_ol_record_values(ol_dict, values, model)
        record = self.env[model].create(record_values)
        values['real_record'] = record
        return record

    @api.model
    def _extract_ol_record_values(self, ol_dict: dict, values: dict, model: str):
        record_values = dict(values)
        extracted_values = self._get_formatted_record_values(ol_dict, record_values, model)
        return extracted_values

    @api.model
    def _extract_families(self, family, ol_dict):
        family = dict(family)
        return self._get_formatted_record_values(ol_dict, family, 'school.family')

    @api.model
    def _extract_students(self, student, ol_dict):
        student = dict(student)
        student_values = self._get_formatted_record_values(ol_dict, student, 'school.student')
        enrollment_history = self._format_enrollment_history(ol_dict, student.pop('enrollment_history', []))
        student_values['enrollment_state_ids'] = [Command.create(status) for status in enrollment_history]
        return student_values

    def _format_enrollment_history(self, ol_dict, enrollment_history_values: list):
        if not enrollment_history_values:
            return []
        enrollment_history_formatted_values = []
        for enrollment_history in enrollment_history_values:
            history_values = self._get_formatted_record_values(ol_dict, enrollment_history, 'school.enrollment.history')

            if not history_values.get('enrollment_status_id', False):
                if 'enrollment_status_id' in enrollment_history and type(enrollment_history['enrollment_status_id']) == dict:
                    status_values = enrollment_history['enrollment_status_id']
                    if 'type' in status_values and type(status_values['type']) == str:
                        enrollment_history_type = status_values['type']
                        enrollment_status = self.env['school.enrollment.status'].search([('type', '=', enrollment_history_type)])
                        history_values['enrollment_status_id'] = enrollment_status.id

            enrollment_history_formatted_values.append(history_values)
        return enrollment_history_formatted_values

    @api.model
    def _extract_individuals(self, individual, ol_dict):
        individual = dict(individual)
        return self._get_formatted_record_values(ol_dict, individual, 'school.family.individual')

    @api.model
    def _get_family_relation_values(self, family, ol_dict, family_real_record):
        student_ids = self._format_field_value('school.family', 'student_ids', family.get('students', []), ol_dict)
        individual_ids = self._format_field_value('school.family', 'individual_ids', family.get('individuals', []), ol_dict)

        return {
            'student_ids': student_ids,
            'individual_ids': individual_ids,
            }

    @api.model
    def _get_student_relation_values(self, student, ol_dict, student_real_record):
        financial_responsibility = []
        student_ids = self._get_student_relationship_values(ol_dict, student.get('student_relationship_ids', []))
        finance_responsibility_field = self.env['school.student']._fields.get('financial_responsibility_ids', False)
        if finance_responsibility_field:
            financial_responsibility_value = self._get_family_responsibility_values(ol_dict, student.get('financial_responsibility_ids', []))
            if not financial_responsibility_value and student_real_record.family_ids:
                financial_responsibility = self._create_financial_responsibility_values(ol_dict, student_real_record.family_ids[0].id)
        return {
            'relationship_ids': student_ids,
            'financial_responsibility_ids': financial_responsibility
        }

    @api.model
    def _get_student_relationship_values(self, ol_dict, relationship_values_list):
        model = 'school.student.relationship'
        relationship_values_list_to_create = []

        for relationship_values in relationship_values_list:
            relationship_values_to_create = self._get_formatted_record_values(ol_dict, relationship_values, model)
            individual = self._format_as_many2one(ol_dict, 'school.family.individual', relationship_values['individual_id'])
            relationship_values_to_create.update({
                'individual_id': individual.id,
                })
            relationship_values_list_to_create.append(Command.create(relationship_values_to_create))
        return relationship_values_list_to_create

    @api.model
    def _get_family_responsibility_values(self, ol_dict, family_responsibility_values):
        model = 'school.financial.responsibility'
        responsibility_values_list_to_update = []

        for responsibility_value in family_responsibility_values:
            responsibility_values_to_create = self._get_formatted_record_values(ol_dict, responsibility_value, model)
            family_id = self._format_as_many2one(ol_dict, 'school.family',
                                                 responsibility_value['family_id'])
            product_categ_id = self._format_as_many2one(ol_dict, 'product.category',
                                                        responsibility_value['product_categ'])
            responsibility_values_to_create.update({
                'family_id': family_id.id,
                'product_category_id': product_categ_id.id
            })
            responsibility_values_list_to_update.append(Command.create(responsibility_values_to_create))
        return responsibility_values_list_to_update

    @api.model
    def _create_financial_responsibility_values(self, ol_dict, family_value):
        responsibility_values_list_to_create = []
        product_category = self.env['product.category'].search([('parent_id', '=', False)])
        family_id = self._format_as_many2one(ol_dict, 'school.family', family_value)
        for category in product_category:
            responsibility_values_list_to_create.append(Command.create({
                'family_id': family_id.id,
                'product_category_id': category.id,
                'percentage': 1.0
            }))
        return responsibility_values_list_to_create

    @api.model
    def _get_formatted_record_values(self, ol_dict: dict, extract_record: dict, model: str):
        values = {}
        for key, value in extract_record.items():
            formatted_value = self._format_field_value(model, key, value, ol_dict)
            if formatted_value:
                values[key] = formatted_value
        return values

    ##############################
    # Compute and search methods #
    ##############################
    @api.depends('generated_json')
    def _compute_resume_record(self):
        ol_dict = json.loads(self.generated_json or '{}')
        self.student = len(ol_dict.get('students', []))
        self.families = len(ol_dict.get('families', []))
        self.individuals = len(ol_dict.get('individuals', []))
        self.districts = len(ol_dict.get('districts', []))
        self.schools = len(ol_dict.get('schools', []))
        self.period_categories = len(ol_dict.get('period_categories', []))
        self.periods = len(ol_dict.get('periods', []))
        self.programs = len(ol_dict.get('programs', []))
        self.grade_level = len(ol_dict.get('grade_levels', []))


class OlMigrationToolMethod(models.Model):
    _name = 'ol.migration.tool.method'
    _description = ' Migration Tool Method'

    name = fields.Char('Method Name', required=True)
    script = fields.Text('Script', required=True)
    generated_json = fields.Text(string="Generated JSON")

    def generate_json(self):
        env = api.Environment(self.env.cr, SUPERUSER_ID, {})
        values_in_script = {'result': {}, 'env': env}
        safe_eval(self.script, values_in_script, mode="exec", nocopy=True)
        return json.dumps(values_in_script['result'], indent=2)

