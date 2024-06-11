# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.fields import Command
from odoo.exceptions import UserError
import requests

_facts_demographics_url = 'https://api.factsmgt.com/people/%i/Demographic'
_facts_person_data_url = 'https://api.factsmgt.com/People/%i'
_facts_person_address_url = 'https://api.factsmgt.com/people/Address/%i'
_facts_person_families_by_personId_url = 'https://api.factsmgt.com/people/PersonFamily?Filters=personId==%s'
_facts_person_families_by_familyId_url = 'https://api.factsmgt.com/people/PersonFamily?Filters=familyId==%s'
_facts_family_data_url = 'https://api.factsmgt.com/families/%s'
_facts_student_data_url = 'https://api.factsmgt.com/Students?Filters=studentId==%s'

_eduweb_student_enrollment_state = 'https://api.eduwebgroup.com/EnrollmentState/%s'
_eduweb_student_relationship = 'https://api.eduwebgroup.com/Person/%s/Relationships'


class SyncStudentWithFacts(models.TransientModel):
    _name = 'sync.student.with.facts'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'student_ids' in fields_list:
            if self._context.get('active_model') == 'school.student':
                res['student_ids'] = self._context.get('active_ids', [])
        return res

    student_ids = fields.Many2many('school.student', required=True)
    demographics_option = fields.Boolean("Demographics", default=True)
    families_option = fields.Boolean("Family", default=True)
    academics_option = fields.Boolean("Academics", default=True)
    family_option_create_if_not_exists = fields.Boolean("Create family if not exists", default=True)
    family_option_update_family = fields.Boolean("Update family", default=True)
    family_option_update_family_individuals = fields.Boolean("Update family individuals", default=True)
    family_option_relationships = fields.Boolean("Update student relationships", default=True)

    def sync_students(self):
        for student in self.student_ids:
            self.with_context(no_program_filter=True).sync_student_data(student)

    def sync_student_data(self, student):
        student_values = {}
        if self.demographics_option:
            student_values.update(self._prepare_individual_demographics(student.facts_id))
        if self.families_option:
            self._update_student_families(student)
        if self.family_option_update_family_individuals and self.family_option_relationships:
            student_values.update(self._prepare_student_relationships(student))
        if self.academics_option:
            # We can use the update method of Command to update the student enrollment state in one transaction... I guess
            student_values.update(self._prepare_individual_academics(student))
        if student_values:
            student.write(student_values)

    def _prepare_individual_demographics(self, individual_facts_id):
        individual_values = {}
        
        # Get Address
        individual_person_response = self._send_facts_api_request(_facts_person_data_url % individual_facts_id)
        individual_person_data = individual_person_response.json()
        
        if individual_person_data.get('addressID', False):
            address_response = self._send_facts_api_request(_facts_person_address_url % individual_person_data['addressID'])
            individual_address_data = address_response.json()
            
            if individual_address_data.get('country', False):
                country = self.get_or_create_country_by_name(individual_address_data['country'])
                individual_values['country_id'] = country.id
                if individual_address_data.get('state', False):
                    state = self.get_or_create_state_in_country_by_name(country, individual_address_data['state'])
                    individual_values['state_id'] = state.id
            
            individual_values.update({
                'street': individual_address_data.get('address1', False),
                'street2': individual_address_data.get('address2', False),
                'city': individual_address_data.get('city', False),
                'zip': individual_address_data.get('zip', False),
                })

        # Get demographics
        individual_demographics_response = self._send_facts_api_request(_facts_demographics_url % individual_facts_id)
        individual_demographics_data = individual_demographics_response.json()

        if 'gender' in individual_demographics_data:
            gender = self.env['school.gender'].search([('key', 'ilike', individual_demographics_data.get('gender', False))], limit=1)
            individual_values['gender'] = gender.id

        individual_values.update({
            'first_name': individual_person_data.get('firstName', False),
            'last_name': individual_person_data.get('lastName', False),
            'middle_name': individual_person_data.get('middleName', False),
            'facts_nickname': individual_person_data.get('nickName', False),
            'salutation': individual_person_data.get('salutation', False),
            'suffix': individual_person_data.get('suffix', False),
            'email': individual_person_data.get('email', False),
            'email2': individual_person_data.get('email2', False),
            'phone': individual_person_data.get('homePhone', False),
            'mobile': individual_person_data.get('cellPhone', False),
            
            'date_of_birth': individual_demographics_data.get('birthdate', False),
            'ethnicity': individual_demographics_data.get('ethnicity', False),
            'citizenship': individual_demographics_data.get('citizenship', False),
            })
        return individual_values

    @api.model
    def get_or_create_country_by_name(self, country_name):
        country = self.env['res.country'].search([('name', '=', country_name)], limit=1)
        if not country:
            country = self.env['res.country'].sudo().create({'name': country_name})
        return country

    @api.model
    def get_or_create_state_in_country_by_name(self, country, state_name):
        state = country.state_ids.filtered_domain([('name', '=', state_name)])[:1]
        if not state:
            state = self.env['res.country.state'].sudo().create({'name': state_name, 'country_id': country.id, 'code': state_name})
        return state

    def _update_student_families(self, student):
        student_family_fact_ids = self._get_student_families(student)
        for family_facts_id in student_family_fact_ids:
            self._sync_family_by_facts_id(family_facts_id)

    def _get_student_families(self, student):
        facts_response = self._send_facts_api_request(_facts_person_families_by_personId_url % student.facts_id)
        if facts_response.status_code == 200:
            facts_result = facts_response.json()['results']
            family_ids = [element['familyId'] for element in facts_result]
            return family_ids
        return []

    def _sync_family_by_facts_id(self, family_facts_id: int):
        family = self.env['school.family'].search([('facts_id', '=', family_facts_id)], limit=1)

        # Test remove family

        if not family:
            # True for testing
            if self.family_option_create_if_not_exists:
                family = self._create_family_by_facts_id(family_facts_id)
        else:
            if self.family_option_update_family:
                self._update_data_family_by_with_facts(family)
        if family:
            if self.family_option_update_family_individuals:
                individuals = self._update_family_individuals_data(family)
                family.write({
                    'individual_with_students_ids': [Command.set(individuals.ids)]
                    })

    def _create_family_by_facts_id(self, family_facts_id):
        family_data_response_data = self._get_family_data_from_facts(family_facts_id)

        family = self.env['school.family'].sudo().create({
            'name': family_data_response_data['familyName'],
            'facts_id': family_facts_id,
            })
        return family

    def _update_data_family_by_with_facts(self, family):
        family_data_response_data = self._get_family_data_from_facts(family.facts_id)
        family.sudo().update({
            'name': family_data_response_data['familyName'],
            })
        return family
    
    def _update_family_individuals_data(self, family):
        individual_facts_ids = self._get_family_individuals(family)
        individuals = self.env['school.family.individual'].sudo()
        for individual_facts_id in individual_facts_ids:
            individual = individuals.search([('facts_id', '=', individual_facts_id)], limit=1)
            if not individual:
                individual = self._create_individual_by_facts_id(individual_facts_id)
            else:
                self._update_individual_with_facts(individual)
            
            if self._check_if_individual_is_student_by_facts_id(individual_facts_id) and not individual.student_ids:
                # We create a student here because it needs to be a student
                self.env['school.student'].sudo().create({'individual_id': individual.id})
            individuals += individual
        return individuals
    
    def _check_if_individual_is_student_by_facts_id(self, individual_facts_id):
        student_data_response = self._send_facts_api_request(_facts_student_data_url % individual_facts_id)
        student_data_response_data = student_data_response.json()
        return student_data_response_data['rowCount'] != 0

    def _get_family_individuals(self, family):
        facts_response = self._send_facts_api_request(_facts_person_families_by_familyId_url % family.facts_id)
        if facts_response.status_code == 200:
            facts_result = facts_response.json()['results']
            person_ids = [element['personId'] for element in facts_result]
            return person_ids
        return []

    def _create_individual_by_facts_id(self, individual_facts_id):
        individual_values = self._prepare_individual_demographics(individual_facts_id)
        individual_values['facts_id'] = individual_facts_id
        return self.env['school.family.individual'].sudo().create(individual_values)

    def _update_individual_with_facts(self, individual):
        individual_values = self._prepare_individual_demographics(individual.facts_id)
        individual.write(individual_values)

    def _prepare_individual_academics(self, student):
        student_enrollment_state_data_response = self._send_eduweb_api_request(_eduweb_student_enrollment_state % student.facts_id)
        student_enrollment_state_data_response_data = student_enrollment_state_data_response.json()
        student_enrollment_state_update_values = []

        for student_enrollment_state_data in student_enrollment_state_data_response_data:
            enrollment_school_code = student_enrollment_state_data['schoolCode']
            enrollment_state_values = self._prepare_enrollment_state_values(student_enrollment_state_data)
            enrollment_state = student.enrollment_state_ids.filtered(lambda es: es.program_id.school_code_name == enrollment_school_code)[:1]

            if enrollment_state:
                student_enrollment_state_update_values.append(Command.update(enrollment_state.id, enrollment_state_values))
            else:
                student_enrollment_state_update_values.append(Command.create(enrollment_state_values))

        if student_enrollment_state_update_values:
            return {'enrollment_state_ids': student_enrollment_state_update_values}
        return {}

    def _prepare_student_relationships(self, student):
        student_relationships_data_response = self._send_eduweb_api_request(_eduweb_student_relationship % student.facts_id)
        student_relationships_data_response_data = student_relationships_data_response.json()
        student_relationships_update_values = []

        for student_relationship_data in student_relationships_data_response_data:
            parent_facts_id = student_relationship_data['parentId']
            relationships_values = self._prepare_relationships_values(student_relationship_data)
            if relationships_values:
                relationship = student.relationship_ids.filtered(lambda rel: rel.individual_id.facts_id == parent_facts_id)[:1]

                if relationship:
                    student_relationships_update_values.append(Command.update(relationship.id, relationships_values))
                else:
                    student_relationships_update_values.append(Command.create(relationships_values))

        if student_relationships_update_values:
            return {'relationship_ids': student_relationships_update_values}
        return {}

    @api.model
    def _prepare_relationships_values(self, student_relationship_data):
        if not student_relationship_data['relationship'] or not student_relationship_data['parentId']:
            return {}
        individual = self.env['school.family.individual'].sudo().search([('facts_id', '=', student_relationship_data['parentId'])], limit=1)
        relationship_type = self.env['school.student.relationship.type'].sudo().search([('type', 'ilike', student_relationship_data['relationship'])], limit=1)
        relationship_values = {
            'individual_id': individual.id,
            'relationship_type_id': relationship_type.id,
            'custody': student_relationship_data['custody'],
            'correspondence': student_relationship_data['correspondence'],
            'family_portal': student_relationship_data['parentsWeb'],
            'is_emergency_contact': student_relationship_data['emergencyContact'],
            }
        return relationship_values

    @api.model
    def _prepare_enrollment_state_values(self, student_enrollment_state_data: dict):

        program = self.env['school.program'].search([('school_id.code', 'ilike', student_enrollment_state_data['schoolCode'])], limit=1)

        if student_enrollment_state_data['gradeLevel']:
            grade_level_id = program.grade_level_ids.filtered_domain([('school_id.code', 'ilike', student_enrollment_state_data['gradeLevel'])])[:1].id
        else:
            grade_level_id = False

        if student_enrollment_state_data['status']:
            status_id = self.env['school.enrollment.status'].search([('type', 'ilike', student_enrollment_state_data['status'])], limit=1)
        else:
            status_id = False

        next_program = self.env['school.program'].search([('school_id.code', 'ilike', student_enrollment_state_data['nextSchoolCode'])], limit=1)

        if student_enrollment_state_data['nextGradeLevel']:
            next_grade_level_id = program.grade_level_ids.filtered_domain([('school_id.code', 'ilike', student_enrollment_state_data['nextGradeLevel'])])[:1].id
        else:
            next_grade_level_id = False

        if student_enrollment_state_data['nextStatus']:
            next_status_id = self.env['school.enrollment.status'].search([('type', 'ilike', student_enrollment_state_data['nextStatus'])], limit=1)
        else:
            next_status_id = False

        return {
            'program_id': program.id,
            'grade_level_id': grade_level_id,
            'enrollment_status_id': status_id,
            'next_program_id': next_program.id,
            'next_grade_level_id': next_grade_level_id,
            'next_enrollment_status_id': next_status_id,
            'enrolled_date': student_enrollment_state_data['enrollDate'],
            'graduation_date': student_enrollment_state_data['graduationDate'],
            'withdraw_date': student_enrollment_state_data['withdrawDate'],
            }

    @api.model
    def _get_family_data_from_facts(self, family_facts_id):
        family_data_response = self._send_facts_api_request(_facts_family_data_url % family_facts_id)
        family_data_response_data = family_data_response.json()
        return family_data_response_data

    @api.model
    def _send_facts_api_request(self, url):
        EdoobFactsHttpUtils = self.env['edoob.facts.http.utils'].sudo()
        return EdoobFactsHttpUtils._send_facts_api_request(url)

    @api.model
    def _send_eduweb_api_request(self, url):
        EdoobFactsHttpUtils = self.env['edoob.facts.http.utils'].sudo()
        return EdoobFactsHttpUtils._send_eduweb_api_request(url)
