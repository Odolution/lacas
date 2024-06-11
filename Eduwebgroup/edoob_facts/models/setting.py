# -*- coding: utf-8 -*-

from odoo import models, fields, _, api
from odoo.fields import Command

from odoo.fields import Datetime as datetime
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)
MAX_SEMESTER = 3


class SchoolBaseSettings(models.TransientModel):
    """  Settings for school module """
    _inherit = "res.config.settings"

    district_code = fields.Char(string=_("District Code"), default="MY-DTRCT",
                                config_parameter='school_facts.district_code',
                                store=True)
    school_codes = fields.Char(string=_("School Codes (Use , as delimiter)"),
                               config_parameter='school_facts.school_codes',
                               default="MY-SCHL1,MY-SCHL2", store=True)

    # configuracion para el api de facts
    facts_api_url = fields.Char(string="FACTS-API URL",
                                config_parameter='school_facts.base_url_facts',
                                default="https://api.factsmgt.com")
    subscription_key = fields.Char(string="Subscription Key",
                                   config_parameter='school_facts.subscription_key',
                                   default="ac2ca997453c4602a9dbd23f77d0ca67")
    facts_api_key = fields.Char(string="FACTS-API Key",
                                config_parameter='school_facts.facts_api_key',
                                default="Insert API-Key...")

    eduweb_api_url = fields.Char(string="Eduweb API URL",
        config_parameter='school_facts.eduweb_api_url',
        default="https://api.eduwebgroup.com")
    eduweb_api_key = fields.Char(string="Eduweb API Key",
        config_parameter='school_facts.eduweb_api_key',
        default="xx-xxxxxxxxxxxxxx")

    country_id = fields.Many2one(
        'res.country',
        config_parameter='school_facts.country_id',
        string='Default Country ID',
        default=lambda self: self.env.company.country_id)

    def create_sync_data(self):
        env = self.sudo().env
        self.ensure_one()

        env['sincro_data_base.api'].search([]).unlink()
        apis = self._ef_create_facts_school_config_api()
        apis += self._ef_create_facts_demographics_api()
        apis += self._ef_create_eduweb_api()

        env['ir.config_parameter'].sudo().set_param("api_configurator_ids", ','.join(map(str, apis.ids)))

    def _prepare_facts_api_header_values(self):
        return [
            {'name': 'Ocp-Apim-Subscription-Key', 'value': self.subscription_key},
            {'name': 'Facts-Api-Key', 'value': self.facts_api_key},
            ]

    def _ef_create_facts_school_config_api(self):
        env = self.sudo().env
        header_values = self._prepare_facts_api_header_values()

        facts_config_api = env['sincro_data_base.api'].sudo().create({
            'name': 'Facts School Config',
            'base_url': self.facts_api_url,
            'header_ids': [Command.create(values) for values in header_values]
            })

        self._ef_create_district_server(facts_config_api)
        self._ef_create_school_server(facts_config_api)
        self._ef_create_enrollment_status_server(facts_config_api)
        return facts_config_api

    def _ef_create_district_server(self, facts_config_api):
        env = self.sudo().env
        school_facts_config_menu = env.ref("edoob_facts.school_facts_config")
        district_data_server = env['sincro_data_base.server'].create({
            'name': "District Data",
            'path': '/SchoolConfigurations',
            'method': 'ws_odoo',
            'state': 'draft',
            'key_json_data': 'results',
            'model_id': env.ref('edoob.model_school_district').id,
            'parent_menu_item_ids': [Command.link(school_facts_config_menu.id)],
            'only_update': True,
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'districtName',
                    'field_id': env.ref('edoob.field_school_district__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_config_api.id,
            })

        district_data_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'static_value',
                    'default_value': self.district_code,
                    'field_id': env.ref('edoob.field_school_district__code').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': district_data_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=0, second=0)
        district_data_server.subscribe(order=1, interval_type='months', interval_number=12, nextcall=nextcall)
        return district_data_server

    def _ef_create_school_server(self, facts_config_api):
        env = self.sudo().env
        school_facts_config_menu = env.ref("edoob_facts.school_facts_config")
        school_server = env['sincro_data_base.server'].create({
            'name': "School Data",
            'path': '/SchoolConfigurations',
            'method': 'ws_odoo',
            'state': 'draft',
            'key_json_data': 'results',
            'only_update': True,
            'model_id': env.ref('edoob.model_school_school').id,
            'parent_menu_item_ids': [Command.link(school_facts_config_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'schoolName',
                    'field_id': env.ref('edoob.field_school_school__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'configSchoolID',
                    'field_id': env.ref('edoob_facts.field_school_school__facts_school_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_config_api.id,
            })

        school_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'schoolCode',
                    'field_id': env.ref('edoob.field_school_school__code').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': school_server.id,

                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=0, second=0)
        school_server.subscribe(order=2, interval_type='months', interval_number=12, nextcall=nextcall)
        return school_server

    def _ef_create_enrollment_status_server(self, facts_config_api):
        env = self.sudo().env
        school_facts_config_menu = env.ref("edoob_facts.school_facts_config")
        school_year_server = env['sincro_data_base.server'].create({
            'name': "Status Data",
            'path': '/Students/Status?PageSize=2147483647',
            'method': 'ws_odoo',
            'state': 'draft',
            'key_json_data': 'results',
            'model_id': env.ref('edoob.model_school_enrollment_status').id,
            'parent_menu_item_ids': [Command.link(school_facts_config_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'displayName',
                    'field_id': env.ref('edoob.field_school_enrollment_status__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'status',
                    'field_id': env.ref('edoob.field_school_enrollment_status__type').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_config_api.id,
            })

        school_year_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'status',
                    'field_id': env.ref('edoob.field_school_enrollment_status__key').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': school_year_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=0, second=0)
        school_year_server.subscribe(order=5, interval_type='months', interval_number=12, nextcall=nextcall)
        return school_year_server

    def _ef_create_facts_demographics_api(self):
        env = self.sudo().env
        header_values = self._prepare_facts_api_header_values()

        facts_demographics_api = env['sincro_data_base.api'].sudo().create({
            'name': "Facts Demographics",
            'base_url': self.facts_api_url,
            'header_ids': [Command.create(values) for values in header_values]
            })

        self._ef_create_families_server(facts_demographics_api)
        self._ef_create_students_server(facts_demographics_api)
        self._ef_create_parents_server(facts_demographics_api)
        self._ef_create_person_update_server(facts_demographics_api)
        self._ef_create_link_person_to_family_server(facts_demographics_api)
        return facts_demographics_api

    def _ef_create_families_server(self, facts_demographics_api):
        env = self.sudo().env
        dem_menu = env.ref("edoob_facts.school_facts_dem")
        families_server = env['sincro_data_base.server'].create({
            'name': "Families Data",
            'path': '/families?PageSize=2147483647',
            'method': 'ws_odoo',
            'state': 'draft',
            'key_json_data': 'results',
            'model_id': env.ref('edoob.model_school_family').id,
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'familyName',
                    'field_id': env.ref('edoob.field_school_family__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'familyNameBP',
                    'field_id': env.ref('edoob_facts.field_school_family__family_name_bp').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_demographics_api.id,
            })

        families_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'familyID',
                    'field_id': env.ref('edoob_facts.field_school_family__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': families_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=10, second=0)
        families_server.subscribe(order=8, interval_type='minutes', interval_number=10, nextcall=nextcall)
        return families_server

    def _ef_create_students_server(self, facts_demographics_api):
        env = self.sudo().env
        dem_menu = env.ref("edoob_facts.school_facts_dem")
        student_server = env['sincro_data_base.server'].create({
            'name': "Student - Create",
            'path': '/Students?PageSize=2147483647',
            'method': 'ws_odoo',
            'state': 'draft',
            'key_json_data': 'results',
            'only_create_item': True,
            'model_id': env.ref('edoob.model_school_student').id,
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'studentId',
                    'concat_value': 'facts_id_%s',
                    'field_id': env.ref('edoob.field_school_student__first_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'studentId',
                    'concat_value': 'facts_id_%s',
                    'field_id': env.ref('edoob.field_school_student__last_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_demographics_api.id,
            })

        student_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'studentId',
                    'field_id': env.ref('edoob_facts.field_school_student__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': student_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=0, second=0)
        student_server.subscribe(order=6, interval_type='minutes', interval_number=10, nextcall=nextcall)
        return student_server

    def _ef_create_parents_server(self, facts_demographics_api):
        env = self.sudo().env
        dem_menu = env.ref("edoob_facts.school_facts_dem")
        parent_server = env['sincro_data_base.server'].create({
            'name': "Parent - Create",
            'path': '/people/ParentStudent?PageSize=2147483647',
            'method': 'ws_odoo',
            'state': 'draft',
            'key_json_data': 'results',
            'model_id': env.ref('edoob.model_school_family_individual').id,
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'only_create_item': True,
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'parentID',
                    'concat_value': 'facts_id_%s',
                    'field_id': env.ref('edoob.field_school_family_individual__first_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'parentID',
                    'concat_value': 'facts_id_%s',
                    'field_id': env.ref('edoob.field_school_family_individual__last_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_demographics_api.id,
            })

        parent_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'parentID',
                    'field_id': env.ref('edoob_facts.field_school_family_individual__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': parent_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=5, second=0)
        parent_server.subscribe(order=7, interval_type='minutes', interval_number=10, nextcall=nextcall)
        return parent_server

    def _ef_create_person_update_server(self, facts_demographics_api):
        env = self.sudo().env
        dem_menu = env.ref("edoob_facts.school_facts_dem")
        person_update_server = env['sincro_data_base.server'].create({
            'name': "Person - Update data",
            'path': '/People?PageSize=2147483647',
            'method': 'ws_odoo',
            'state': 'draft',
            'key_json_data': 'results',
            'only_update': True,
            'model_id': env.ref('edoob.model_school_family_individual').id,
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'firstName',
                    'field_id': env.ref('edoob.field_school_family_individual__first_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'lastName',
                    'field_id': env.ref('edoob.field_school_family_individual__last_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'middleName',
                    'field_id': env.ref('edoob.field_school_family_individual__middle_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'nickName',
                    'field_id': env.ref('edoob_facts.field_school_family_individual__facts_nickname').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'salutation',
                    'field_id': env.ref('edoob_facts.field_school_family_individual__salutation').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'suffix',
                    'field_id': env.ref('edoob_facts.field_school_family_individual__suffix').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'email',
                    'field_id': env.ref('edoob.field_school_family_individual__email').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'cellPhone',
                    'field_id': env.ref('edoob.field_school_family_individual__mobile').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'homePhone',
                    'field_id': env.ref('edoob.field_school_family_individual__phone').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_demographics_api.id,
            })

        person_update_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'personId',
                    'field_id': env.ref('edoob_facts.field_school_family_individual__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': person_update_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=15, second=0)
        person_update_server.subscribe(order=9, interval_type='minutes', interval_number=30, nextcall=nextcall)
        return False

    def _ef_create_link_person_to_family_server(self, facts_demographics_api):
        env = self.sudo().env
        dem_menu = env.ref("edoob_facts.school_facts_dem")
        link_person_to_family_server = env['sincro_data_base.server'].create({
            'name': "Link Person to Family",
            'path': '/people/PersonFamily?PageSize=2147483647',
            'method': 'ws_odoo',
            'state': 'draft',
            'key_json_data': 'results',
            'only_update': True,
            'model_id': env.ref('edoob.model_school_family_individual').id,
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'familyId',
                    'field_id': env.ref('edoob.field_school_family_individual__family_ids').id,
                    'key_field_id': env.ref('edoob_facts.field_school_family__facts_id').id,
                    'is_active': True,
                    'force_overwrite': False,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_demographics_api.id,
            })

        link_person_to_family_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'personId',
                    'field_id': env.ref('edoob_facts.field_school_family_individual__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': link_person_to_family_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=15, second=0)
        link_person_to_family_server.subscribe(order=10, interval_type='minutes', interval_number=15, nextcall=nextcall)
        return link_person_to_family_server

    # Eduweb
    def _prepare_eduweb_api_header_values(self):
        return [
            {
                'name': 'api-key',
                'value': self.eduweb_api_key
                }
            ]

    def _ef_create_eduweb_api(self):
        env = self.sudo().env
        header_values = self._prepare_eduweb_api_header_values()
        eduweb_api = env['sincro_data_base.api'].sudo().create({
            'name': "Eduweb API",
            'base_url': self.eduweb_api_url,
            'header_ids': [Command.create(values) for values in header_values]
            })
        self._ef_create_grade_level_server(eduweb_api)
        self._ef_create_person_photo_server(eduweb_api)
        self._ef_create_accounting_system_server(eduweb_api)
        self._ef_create_finance_responsibility_server(eduweb_api)
        self._ef_create_family_invoice_address_server(eduweb_api)
        self._ef_create_person_relationships_server(eduweb_api)
        self._ef_create_enrollment_state(eduweb_api)
        self._ef_create_person_address(eduweb_api)
        return eduweb_api

    def _ef_create_grade_level_server(self, eduweb_api):
        env = self.sudo().env
        grade_level_menu = env.ref("edoob_facts.school_facts_config")
        grade_level_server = env['sincro_data_base.server'].create({
            'name': 'Grade level',
            'path': '/gradelevel',
            'method': 'ws_odoo',
            'state': 'draft',
            'model_id': env.ref('edoob.model_school_grade_level').id,
            'model_name': 'school.grade.level',
            'parent_menu_item_ids': [Command.link(grade_level_menu.id)],
            'mapped_field_ids': [Command.create({
                'json_key': 'active',
                'field_id': env.ref(
                    'edoob.field_school_grade_level__active').id,
                'is_active': True,
                'force_overwrite': True,
                }), ],
            'include_archived': True,
            'api_id': eduweb_api.id,
            })
        grade_level_server.update({
            'ws_odoo_field_key_ids': [Command.create({
                'json_key': 'gradeLevelName',
                'field_id': env.ref(
                    'edoob.field_school_grade_level__name').id,
                'is_active': True,
                'force_overwrite': True,
                'server_id': grade_level_server.id,
                }), Command.create({
                'json_key': 'schoolCode',
                'field_id': env.ref(
                    'edoob.field_school_grade_level__program_id').id,
                'key_field_id': env.ref(
                    'edoob_facts.field_school_program__school_code_name').id,
                'is_active': True,
                'force_overwrite': True,
                'server_id': grade_level_server.id,
                }), ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=0, second=0)
        grade_level_server.subscribe(order=3, interval_type='months', interval_number=12, nextcall=nextcall)
        return grade_level_server

    def _ef_create_person_photo_server(self, eduweb_api):
        env = self.sudo().env
        facts_photos_menu = env.ref("edoob_facts.school_facts_photos")
        person_photo_server = env['sincro_data_base.server'].create({
            'name': "Person's Photo",
            'path': '/person/pictures',
            'method': 'ws_odoo',
            'state': 'draft',
            'only_update': True,
            'model_id': env.ref('edoob.model_school_family_individual').id,
            'parent_menu_item_ids': [Command.link(facts_photos_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'pathToPicture',
                    'concat_value': f"https://renweb1.renweb.com/ftp/{self.district_code}/pictures/%s",
                    'is_an_img_from_url': True,
                    'field_id': env.ref('edoob.field_school_family_individual__image_1920').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': eduweb_api.id,
            'is_active_skip_limit': True,
            'limit': 400,
            })
        person_photo_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'personId',
                    'field_id': env.ref('edoob_facts.field_school_family_individual__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': person_photo_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=1, minute=15, second=0)
        person_photo_server.subscribe(order=16, interval_type='minutes', interval_number=15, nextcall=nextcall)
        return person_photo_server

    # noinspection PyUnresolvedReferences
    # Person Address, Change Family Invoice Address finance responsibility
    def _ef_create_enrollment_state(self, eduweb_api):
        env = self.sudo().env
        dem_menu = env.ref("edoob_facts.school_facts_dem")
        enrollment_state_server = env['sincro_data_base.server'].create({
            'name': "Enrollment State",
            'path': '/EnrollmentState',
            'method': 'ws_odoo',
            'state': 'draft',
            'model_id': env.ref('edoob.model_school_student_enrollment_state').id,
            'model_name': 'school.student.enrollment.state',
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'gradeLevel',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__grade_level_id').id,
                    'key_field_id': env.ref('edoob.field_school_grade_level__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'status',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__enrollment_status_id').id,
                    'key_field_id': env.ref('edoob.field_school_enrollment_status__type').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'letter_case': 'lower',
                    }),
                Command.create({
                    'json_key': 'nextSchoolCode',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__next_program_id').id,
                    'key_field_id': env.ref('edoob_facts.field_school_program__school_code_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'nextGradeLevel',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__next_grade_level_id').id,
                    'key_field_id': env.ref('edoob.field_school_grade_level__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'nextStatus',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__next_enrollment_status_id').id,
                    'key_field_id': env.ref('edoob.field_school_enrollment_status__type').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'letter_case': 'lower',
                    }),
                Command.create({
                    'json_key': 'enrollDate',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__enrolled_date').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'graduationDate',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__graduation_date').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'withdrawDate',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__withdraw_date').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': eduweb_api.id,
            })
        enrollment_state_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'studentId',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__student_id').id,
                    'key_field_id': env.ref('edoob_facts.field_school_student__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': enrollment_state_server.id,
                    }),
                Command.create({
                    'json_key': 'schoolCode',
                    'field_id': env.ref('edoob.field_school_student_enrollment_state__program_id').id,
                    'key_field_id': env.ref('edoob_facts.field_school_program__school_code_name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': enrollment_state_server.id,
                    }),
                ],
            })
        nextcall = datetime.today() + relativedelta(hour=1, minute=0, second=0)
        enrollment_state_server.subscribe(order=13, interval_type='days', interval_number=1, nextcall=nextcall)
        return enrollment_state_server

    def _ef_create_person_address(self, eduweb_api):
        env = self.sudo().env
        dem_menu = env.ref("edoob_facts.school_facts_dem")
        person_address_server = env['sincro_data_base.server'].create({
            'name': "Person address",
            'path': '/Address',
            'method': 'ws_odoo',
            'state': 'draft',
            'model_id': env.ref('base.model_res_partner').id,
            'only_update': True,
            'model_name': 'res.partner',
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'topPersonLinkId',
                    'field_domain': "[('facts_id', '!=', personId)]",
                    'field_id': env.ref('edoob.field_res_partner__address_partner_link_id').id,
                    'key_field_id': env.ref('edoob_facts.field_res_partner__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'country',
                    'field_id': env.ref('base.field_res_partner__country_id').id,
                    'key_field_id': env.ref('base.field_res_country__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'state',
                    'field_id': env.ref('base.field_res_partner__state_id').id,
                    'key_field_id': env.ref('base.field_res_country_state__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'street1',
                    'field_id': env.ref('base.field_res_partner__street').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'street2',
                    'field_id': env.ref('base.field_res_partner__street2').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'city',
                    'field_id': env.ref('base.field_res_partner__city').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'zip',
                    'field_id': env.ref('base.field_res_partner__zip').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': eduweb_api.id,
            })
        person_address_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'personId',
                    'field_id': env.ref('edoob_facts.field_res_partner__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': person_address_server.id,
                    }),
                ],
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=45, second=0)
        person_address_server.subscribe(order=15, interval_type='hours', interval_number=2, nextcall=nextcall)
        return person_address_server

    def _ef_create_accounting_system_server(self, eduweb_api):
        env = self.sudo().env
        school_facts_config_menu = env.ref("edoob_facts.school_facts_config")

        accounting_system_server = env['sincro_data_base.server'].create({
            'name': "Accounting System",
            'path': '/Finance/AccountingSystem',
            'method': 'ws_odoo',
            'state': 'draft',
            'model_id': env.ref('product.model_product_category').id,
            'model_name': 'product.category',
            'parent_menu_item_ids': [Command.link(school_facts_config_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'name',
                    'field_id': env.ref('product.field_product_category__name').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'schoolCode',
                    'field_id': env.ref('edoob_facts.field_product_category__facts_school_code').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': eduweb_api.id,
            })
        accounting_system_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'id',
                    'field_id': env.ref('edoob_facts.field_product_category__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': accounting_system_server.id,
                    }),
                Command.create({
                    'json_key': 'static_value',
                    'default_value': self.district_code,
                    'field_id': env.ref('edoob_finance.field_product_category__district_id').id,
                    'key_field_id': env.ref('edoob.field_school_district__code').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': accounting_system_server.id,
                    }),
                Command.create({
                    'json_key': 'static_value',
                    'default_value': self.district_code,
                    'field_domain': f"[('parent_id', '=', {env.ref('product.product_category_all').id})]",
                    'field_id': env.ref('product.field_product_category__parent_id').id,
                    'key_field_id': env.ref('edoob_finance.field_product_category__district_code').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': accounting_system_server.id,
                    })
                ],
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=0, second=0)
        accounting_system_server.subscribe(order=4, interval_type='months', interval_number=12, nextcall=nextcall)
        return accounting_system_server

    def _ef_create_finance_responsibility_server(self, eduweb_api):
        env = self.sudo().env
        dem_menu = env.ref("edoob_facts.school_facts_dem")
        financial_responsibility_server = env['sincro_data_base.server'].create({
            'name': "Person - Financial Responsibility Percentage",
            'path': '/Person/Finance/FinancialResponsibilityPercentage',
            'method': 'ws_odoo',
            'state': 'draft',
            'model_id': env.ref('edoob_finance.model_school_financial_responsibility').id,
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'percentage',
                    'field_id': env.ref('edoob_finance.field_school_financial_responsibility__percentage').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': eduweb_api.id,
            })
        financial_responsibility_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'personId',
                    'field_id': env.ref('edoob_finance.field_school_financial_responsibility__student_id').id,
                    'key_field_id': env.ref('edoob_facts.field_school_student__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': financial_responsibility_server.id,
                    }),
                Command.create({
                    'json_key': 'familyId',
                    'field_id': env.ref('edoob_finance.field_school_financial_responsibility__family_id').id,
                    'key_field_id': env.ref('edoob_facts.field_school_family__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': financial_responsibility_server.id,
                    }),
                Command.create({
                    'json_key': 'accountingSystemId',
                    'field_domain': f"[('district_code', '=', '{self.district_code}')]",
                    'field_id': env.ref('edoob_finance.field_school_financial_responsibility__product_category_id').id,
                    'key_field_id': env.ref('edoob_facts.field_product_category__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': financial_responsibility_server.id,
                    }),
                ],
            })
        nextcall = datetime.today() + relativedelta(hour=12, minute=0, second=0)
        financial_responsibility_server.subscribe(order=14, interval_type='hours', interval_number=12, nextcall=nextcall)
        return financial_responsibility_server

    def _ef_create_family_invoice_address_server(self, facts_demographics_api):
        env = self.sudo().env
        dem_menu = self.env.ref("edoob_facts.school_facts_dem")
        family_invoice_address_server = env['sincro_data_base.server'].create({
            'name': "Family - Invoice Address",
            'path': '/Family/InvoiceAddress',
            'method': 'ws_odoo',
            'state': 'draft',
            'only_update': True,
            'model_id': env.ref('edoob.model_school_family').id,
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'invoiceAddressId',
                    'field_id': env.ref('edoob_finance.field_school_family__invoice_address_id').id,
                    'key_field_id': env.ref('edoob_facts.field_res_partner__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_demographics_api.id,
            })

        family_invoice_address_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'familyId',
                    'field_id': env.ref('edoob_facts.field_school_family__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': family_invoice_address_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=45, second=0)
        family_invoice_address_server.subscribe(order=14, interval_type='hours', interval_number=2, nextcall=nextcall)
        return family_invoice_address_server

    def _ef_create_person_relationships_server(self, facts_demographics_api):
        env = self.sudo().env
        dem_menu = self.env.ref("edoob_facts.school_facts_dem")
        person_relationships_server = env['sincro_data_base.server'].create({
            'name': "Person - Relationships",
            'path': '/Person/Relationships',
            'method': 'ws_odoo',
            'state': 'draft',
            'model_id': env.ref('edoob.model_school_student_relationship').id,
            'parent_menu_item_ids': [Command.link(dem_menu.id)],
            'mapped_field_ids': [
                Command.create({
                    'json_key': 'relationship',
                    'field_id': env.ref('edoob.field_school_student_relationship__relationship_type_id').id,
                    'key_field_id': env.ref('edoob.field_school_student_relationship_type__type').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'custody',
                    'field_id': env.ref('edoob.field_school_student_relationship__custody').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'financialResponsibility',
                    'field_id': env.ref('edoob_finance.field_school_student_relationship__invoice_recipient').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'emergencyContact',
                    'field_id': env.ref('edoob.field_school_student_relationship__is_emergency_contact').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'correspondence',
                    'field_id': env.ref('edoob.field_school_student_relationship__correspondence').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                Command.create({
                    'json_key': 'parentsWeb',
                    'field_id': env.ref('edoob.field_school_student_relationship__family_portal').id,
                    'is_active': True,
                    'force_overwrite': True,
                    }),
                ],
            'include_archived': True,
            'api_id': facts_demographics_api.id,
            })

        person_relationships_server.update({
            'ws_odoo_field_key_ids': [
                Command.create({
                    'json_key': 'parentId',
                    'field_id': env.ref('edoob.field_school_student_relationship__individual_id').id,
                    'key_field_id': env.ref('edoob_facts.field_school_family_individual__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': person_relationships_server.id,
                    }),
                Command.create({
                    'json_key': 'studentId',
                    'field_id': env.ref('edoob.field_school_student_relationship__student_id').id,
                    'key_field_id': env.ref('edoob_facts.field_school_student__facts_id').id,
                    'is_active': True,
                    'force_overwrite': True,
                    'server_id': person_relationships_server.id,
                    }),
                ]
            })
        nextcall = datetime.today() + relativedelta(hour=0, minute=45, second=0)
        person_relationships_server.subscribe(order=12, interval_type='hours', interval_number=2, nextcall=nextcall)
        return person_relationships_server


    @api.model
    def _ef_create_district(self, district_code):
        env = self.sudo().env
        district = env['school.district'].create({
            'code': district_code,
            'name': district_code
            })

        self._ef_create_district_product_categories(district)

        return district

    @api.model
    def _ef_create_district_product_categories(self, district):
        env = self.sudo().env
        product_category_env = env['product.category']
        if not district.product_category_ids:
            return product_category_env.create({
                'district_id': district.id,
                'name': _("Parent category of district %s", district.name),
                'parent_id': env.ref('product.product_category_all').id,
                })
        # We return an empty env to make life easier to future developers that want to inherit this method.
        return product_category_env

    def _remove_unused_default_school_structure(self):
        env = self.sudo().env
        district = env.ref('edoob.my_district', raise_if_not_found=False)
        if district:
            for school in district.school_ids:
                for program in school.program_ids:
                    grade_level_ids = program.grade_level_ids.ids
                    enrollment_histories = env[
                        'school.enrollment.history'].search(
                        [('grade_level_id', 'in', grade_level_ids)])
                    if not enrollment_histories:
                        program.grade_level_ids.unlink()
                        program.period_ids.unlink()
                        program.unlink()
                if not school.program_ids:
                    school.unlink()
            if not district.school_ids:
                district.unlink()

    def sync_periods_from_facts(self):
        all_programs = self.env['school.program'].search([('school_code_name', '!=', False)])
        for program in all_programs:
            self._sync_program_periods(program)

    def _sync_program_periods(self, program):
        school_year_data_url = 'https://api.factsmgt.com/SchoolYears?PageSize=2147483647&Filters=schoolCode==%s'
        school_term_data_url = 'https://api.factsmgt.com/SchoolTerms/v2/schools/%s?PageSize=2147483647'
        
        facts_school_id = program.school_id.facts_school_id
        
        SchoolPeriodEnv = self.env['school.period'].sudo()
        EdoobFactsHttpUtils = self.env['edoob.facts.http.utils'].sudo()
        
        school_year_data_response = EdoobFactsHttpUtils._send_facts_api_request(school_year_data_url % program.school_code_name)
        school_year_term_data_response = EdoobFactsHttpUtils._send_facts_api_request(school_term_data_url % (facts_school_id))

        school_year_data_list = school_year_data_response.json()
        school_year_term_data_list = school_year_term_data_response.json()

        school_year_category = self.sudo().env.ref('edoob_facts.period_category_facts_year')
        school_semester_category = self.sudo().env.ref('edoob_facts.period_category_facts_semester')
        school_term_category = self.sudo().env.ref('edoob_facts.period_category_facts_term')
        
        for i, school_year_data in enumerate(school_year_data_list['results']):
            _logger.info(f"Syncing school year [{i+1}/{len(school_year_data_list['results'])}] for {program.school_id.name} -> {school_year_data['yearName']}")
            yearId = school_year_data['yearId']
            school_year = SchoolPeriodEnv.search([('facts_year_id', '=', yearId), ('program_id', '=', program.id)], limit=1)
            if not school_year:
                school_year = SchoolPeriodEnv.create({
                    'name': school_year_data['yearName'],
                    'program_id': program.id, 
                    'category_id': school_year_category.id,
                    'date_start': school_year_data['firstDay'],
                    'date_end': school_year_data['lastDay'],
                    'facts_year_id': yearId
                    })
            
            # Semester meaning:
            # 0 = Year
            # 1,2,3 = Semester 1, Semester 2, Semester 3
            # Sync term data related to year:
            for j, school_year_term_data in enumerate(school_year_term_data_list['results']):
                if school_year_term_data['yearID'] != yearId:
                    continue
                _logger.info(f"Syncing term [{j+1}/{len(school_year_term_data_list['results'])}] for {program.school_id.name} -> {school_year_term_data['name']}")
                if school_year_term_data['semesterID'] == 0:
                    category = school_term_category
                else:
                    category = school_semester_category

                unique_term_id = school_year_term_data['uniqueTermID']
                school_term = SchoolPeriodEnv.search([('facts_unique_term_id', '=', unique_term_id), ('program_id', '=', program.id), ('parent_id', '=', school_year.id)], limit=1)
                if not school_term:
                    school_term = SchoolPeriodEnv.create({
                        'facts_unique_term_id': unique_term_id,
                        'parent_id': school_year.id,
                        'program_id': program.id,
                        'name': school_year_term_data['name'],
                        'date_start': school_year_term_data['firstDay'],
                        'date_end': school_year_term_data['lastDay'],
                        'category_id': category.id,
                        'facts_semester_id': school_year_term_data['semesterID']
                        })
