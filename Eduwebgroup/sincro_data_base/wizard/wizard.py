from odoo import models, api, fields
from odoo.exceptions import UserError

import requests
import logging
import traceback
import json

_logger = logging.getLogger(__name__)

class SyncButton(models.TransientModel):
    _name = 'sincro_data_base.syncbutton.wizard'
    
    import_option = fields.Selection([('all', 'Update all data'), ('only_new', 'Only new data')], string='Select', default='all')
    

    def sync_data(self):
        if 'type' in self._context and self._context['type'] == 'general_view':
            #model_name = self._context['model_name'] or False
            # tomamos desde el contexto el id del boton del menu para identificar cuales son los request asociados a este.
            menu_id = self._context.get('menu_id') or False
            if menu_id:
                active_server_ids = self.env['sincro_data_base.server'].search(
                    # [('state', '=', 'subscribed'), ('model_name', '=', model_name), ('parent_menu_item_id', '=',menu_id)])
                    [('state', '=', 'subscribed'), ('parent_menu_item_ids', 'in', menu_id)])
                # esto limita mucho a la hora de las claves ya que solo se puede controlar 1 static _value en las claves del server
                # esto va a tomar los server en el orden de la sequencia que este establecido
                created_items = []
                for server in active_server_ids:
                    headers = {}
                    for header in server.api_header_ids:
                        headers[header.name] = header.value

                    created_items = server.update_data_ws_odoo(headers, False, self.import_option == 'only_new',
                                                               created_items)
        else:
            model_name = self._context['active_model'] if 'active_model' in self._context  else False
            active_ids = self._context['active_ids']
            records = self.env[model_name].browse(active_ids)
            self._update_records(records)
                
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    @api.model
    def _update_records(self, records):
        for record in records:
            self._update_recursively_record_depending_on_inherits(record)
    
    @api.model
    def _update_recursively_record_depending_on_inherits(self, record):
        for model_name, field_name in record._inherits.items():
            new_record = record[field_name]
            if new_record != record:
                self._update_recursively_record_depending_on_inherits(new_record)
        self._synch_record_with_its_servers(record)
    
    @api.model
    def _synch_record_with_its_servers(self, record):

        if record._name == 'school.student':
            _logger.info(f"Synching student: {record.name}[{record}]")
            self._synch_record_with_student(record)

        active_server_ids = self.env['sincro_data_base.server'].search([('state', '=', 'subscribed'), ('model_name', '=', record._name)])
        for i, server in enumerate(active_server_ids):
            # We filter those record that doesn't match the static key
            if self._does_record_not_match_static_key_values_in_server(record, server):
                continue

            _logger.info(f"[{i+1}/{len(active_server_ids)}] Synching the following record by the wizard: {record.name}[{record}] -> Server: {server.name}[{server}]")
            headers = self._compute_headers(server)
            json_keys = self._get_json_keys_values_to_update(record, server)
            _logger.info(f"Headers: {headers}\nJsonKeys: {json_keys}")
            server.update_data_ws_odoo(headers, json_keys)

    @api.model
    def _does_record_not_match_static_key_values_in_server(self, record, server):
        static_value_do_not_match = False
        static_keys = server.ws_odoo_field_key_ids.filtered(lambda f: f.json_key == 'static_value')
        for static_key in static_keys:
            field_name = static_key.field_id.name
            if field_name in record._fields and record[field_name] != static_key.default_value:
                static_value_do_not_match = True
                break
        return static_value_do_not_match

    @api.model
    def _get_json_keys_values_to_update(self, record, server):
        json_keys = {}
        for itm in server.ws_odoo_field_key_ids:
            if itm.json_key != 'static_value':
                json_keys[itm.json_key] = record[itm.field_id.name]
        return json_keys
    
    @api.model
    def _synch_record_with_student(self, student):
        self._synch_student_family(student)
        self._synch_enrollment_state_to_student(student)
        self._synch_relationships_to_student(student)
    
    @api.model
    def _synch_enrollment_state_to_student(self, student):
        enrollment_state_server = self.env['sincro_data_base.server'].search([
            ('state', '=', 'subscribed'),
            ('model_name', '=', 'school.student.enrollment.state'),
            ('ws_odoo_field_key_ids.field_id.name', '=', 'student_id'), 
            ])
        headers = self._compute_headers(enrollment_state_server)
        enrollment_state_server.update_data_ws_odoo(headers, {'studentId': student.facts_id})
    
    @api.model
    def _synch_student_family(self, student):
        family_ids = self._get_student_families(student)
        if family_ids:
            families_server = self.env['sincro_data_base.server'].search([
                ('state', '=', 'subscribed'),
                ('model_name', '=', 'school.family'),
                ('mapped_field_ids.json_key', '=', 'familyID'), 
                ])
            headers = self._compute_headers(families_server)
            for family_id in family_ids:
                families_server.update_data_ws_odoo(headers, {'familyID': family_id})

    @api.model
    def _get_student_families(self, student):
        ConfigParam = self.env['ir.config_parameter'].sudo()
        get_person_family_url = f"https://api.factsmgt.com/people/PersonFamily?Filters=personId=={student.facts_id}"
        subscription_key = ConfigParam.get_param('school_facts.subscription_key')
        api_key = ConfigParam.get_param('school_facts.facts_api_key')

        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Facts-Api-Key': api_key
            }
        facts_response = requests.get(get_person_family_url, headers=headers)
        if facts_response.status_code == 200:
            facts_result = facts_response.json()['results']
            family_ids = [element['familyId'] for element in facts_result]
            return family_ids
        return []
    
    @api.model
    def _synch_relationships_to_student(self, student):
        relationships_server = self.env['sincro_data_base.server'].search([
            ('state', '=', 'subscribed'),
            ('model_name', '=', 'school.student.relationship'),
            ('ws_odoo_field_key_ids.field_id.name', '=', 'student_id'), 
            ])
        headers = self._compute_headers(relationships_server)
        relationships_server.update_data_ws_odoo(headers, {'studentId': student.facts_id})

    @api.model
    def _compute_headers(self, server):
        headers = {}
        for header in server.api_header_ids:
            headers[header.name] = header.value
        return headers