# -*- coding:utf-8 -*-

import base64
import json
import logging
from datetime import datetime

import requests

import odoo
import odoo.modules.registry
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

# from doc._extensions.html_domain import address

_logger = logging.getLogger(__name__)

REGEX_EMAIL = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
MAX_INT = 2147483647
MAX_ITEMS_BY_THREAT = 300


class SincroDataServer(models.Model):
    _name = "sincro_data_base.server"
    _description = "Sincro Data Server"
    _order = "sequence"

    sequence = fields.Integer(readonly=True, default=-1)
    name = fields.Char(string="Name", required=True)
    api_name = fields.Char(string="Request Name", related="api_id.name", readonly=True)
    api_base_url = fields.Char(string="Base URL", related="api_id.base_url", readonly=True)
    api_header_ids = fields.Many2many(string="API headers", related="api_id.header_ids", readonly=True)
    model_id = fields.Many2one("ir.model", string="Model", required=True, ondelete='cascade')
    api_id = fields.Many2one("sincro_data_base.api", string="API", ondelete='cascade', required=True)
    path = fields.Char(string="Path")
    domain = fields.Char("Domain")
    test_item_model_id = fields.Integer('Item ID')
    parameter_ids = fields.Many2many("sincro_data_base.parameter", "request_id", string="Parameters")
    computed_path = fields.Char(string="Computed path", compute="_compute_path", readonly=True)

    state = fields.Selection(
        [("draft", "Draft"), ("subscribed", "Subscribed")],
        required=True,
        default="draft",
        )
    method = fields.Selection([
        ('get', "GET"),
        ('post', "POST"),
        ('put', "PUT"),
        ('delete', "DELETE"),
        ('patch', "PATCH"),
        ('head', "HEAD"),
        ('connect', "CONNECT"),
        ('options', "OPTIONS"),
        ('trace', "TRACE"),
        ('ws_odoo', "WService -> ODOO"),
        ('odoo_ws', "ODOO -> WService"),
        ],
        string="Method", default='get')
    json_pretty = fields.Boolean("Pretty JSON", default=False)
    json_configuration_id = fields.Many2one('sincro_data_base.configuration_panel', string="JSON Configuration")
    json_example = fields.Char(string='JSON Example', compute="_compute_json", readonly=True)
    response_message = fields.Char(string='Response TEXT', compute="_clean_response", store=True, readonly=True)
    response_code = fields.Integer(string="Response code")
    # json_example = fields.Char(string='JSON Example')
    cron_id = fields.Many2one('ir.cron', string="Cron",
                              ondelete="cascade")

    cron_active = fields.Boolean(string="Active", related='cron_id.active')

    interval_minutes = fields.Integer(string="Interval minutes", default=30)

    retrieve_date = fields.Datetime(string="Last Retrieval Date",
                                    readonly=True)

    log_ids = fields.Many2many(string="Created Families",
                               comodel_name="sincro_data_base.log",
                               relation="sincro_data_base_log_rel", store=True)

    skip = fields.Integer(string="Skip")
    limit = fields.Integer(string="Limit",
                           default=100)

    model_name = fields.Char(string="Model Name", store=True, related='model_id.model')
    retrieve_date_test = fields.Datetime(string="Last Test Date",
                                         readonly=True)

    mapped_field_ids = fields.One2many('sincro_data_base.mapped', 'server_id', string="Mapped fields")

    struct_response = fields.Char("Struct response", store=True)
    ws_json = fields.Char("WS JSON", store=True)
    ws_odoo_field_key = fields.Many2one('ir.model.fields', string='External-odoo Field Key', store=True)
    ws_odoo_field_key_ids = fields.Many2many(
        'sincro_data_base.mapped', relation='sincro_data_base_ws_odoo_field_key_ids_rel',
        string='External-ODOO Field Keys', store=True,
        domain="[('id','in', 'mapped_field_ids')]")
    ws_odoo_cascade_key_ids = fields.Many2many(
        comodel_name='sincro_data_base.mapped',
        relation="sincro_data_base_ws_odoo_cascade_fields_rel",
        domain="[('id','in', 'mapped_field_ids')]",
        string='Cascade Field Keys', store=True)
    key_json_data = fields.Char("JSON Key Data")
    ws_method = fields.Selection([
        ('get', "GET"),
        ('post', "POST"),
        ('put', "PUT"),
        ('delete', "DELETE"),
        ('patch', "PATCH"),
        ('head', "HEAD"),
        ('connect', "CONNECT"),
        ('options', "OPTIONS"),
        ('trace', "TRACE")
    ], string="WS Method", default='get')

    act_window_id = fields.Many2one('ir.actions.act_window', string='Action Window')
    parent_act_window_id = fields.Many2one('ir.actions.act_window', string='Action Window')

    parent_menu_item_id = fields.Many2one('ir.ui.menu', string='Menu Item')

    parent_menu_item_ids = fields.Many2many(
        'ir.ui.menu',
        relation='menu_item_server_rel',
        column1='server_id',
        column2='menu_id')

    view_id = fields.Many2one('ir.ui.view', string='View')

    is_active_skip_limit = fields.Boolean('Use SKip and Limit?', default=False)
    is_save_in_log = fields.Boolean('Save in Log?', default=True)
    parent_menu_id = fields.Many2one('ir.ui.menu', string='Parent Menu Sync', ondelete='Restrict')
    only_update = fields.Boolean('Only Update Item', default=False)
    only_create_item = fields.Boolean('Only Create Item', default=False)

    total_request = fields.Integer("Total request", readonly=True)
    include_archived = fields.Boolean("Include archive records")

    context = fields.Char(string="Context")

    def write(self, values):
        if 'mode_thread' in self._context:
            return True
        return super().write(values)

    def _get_format_json(self, key, value, num_spaces):
        # es una lista
        if isinstance(value, list):
            return '\n%s"%s":%s' % (''.ljust(num_spaces), key, '"[{...},{...},{...},...]",')
        # es un diccionario
        elif isinstance(value, dict):
            inner_value = ''
            for key_inner, data in value.items():
                inner_value += '%s,' % self._get_format_json(key_inner, data, num_spaces + 5)

            dict_lbl = ''
            if key:
                dict_lbl = '%s%s:\n' % (''.ljust(num_spaces), key)

            return '\n%s%s{%s\n%s}' % (dict_lbl, ''.ljust(num_spaces), inner_value, ''.ljust(num_spaces))
        # de ñlo cotnrario devolvemos el value
        else:
            return '\n%s"%s":%s' % (''.ljust(num_spaces), key, str(value))

    def _get_keys_mapped(self, key, value, prefix):
        if isinstance(value, dict):
            inner_list = []
            for key_inner, data in value.items():
                res = self._get_keys_mapped(key_inner, data, '%s' % key)
                # si es una lista entonces las combinamos
                if isinstance(res, list):
                    inner_list += res
                else:
                    if res:
                        inner_list.append(res)
                # += '%s,' % self._get_format_json(key_inner, data, num_spaces + 5)
            return inner_list
        # de ñlo cotnrario devolvemos el valuel
        else:
            return '%s/%s' % (prefix, key) if prefix else str(key)

    

    def indent_json(self):
        # ya tiene formato se lo quitamos
        if '\n' in self.struct_response:
            self.struct_response = self.struct_response.replace('\n', '').replace(' ', '')
            return
        # le damos el formato de tipo json
        aux_struct_response = '['
        for item in json.loads(self.struct_response):
            aux_struct_response += '\n     {'
            for key, value in item.items():
                aux_struct_response += '\n          "%s":' % key
                if isinstance(value, list):
                    aux_struct_response += '"[{...},{...},{...},...]",'
                else:
                    aux_struct_response += '"%s",' % value
            aux_struct_response = aux_struct_response[:-1] + '\n     },'
        aux_struct_response = aux_struct_response[:-1] + '\n]'

        self.struct_response = aux_struct_response

    def add_mapped_field(self):
        created_mapped = self.env["sincro_data_base.mapped"].sudo().create({
            'json_key': 'static_value',
            'server_id': self.id,
        })
        self.mapped_field_ids = [(4, created_mapped.id)]

    def add_json_mapped_field(self):
        created_mapped = self.env["sincro_data_base.mapped"].sudo().create({
            'json_key': 'Write a key of json data',
            'server_id': self.id,
            'is_default': False,
        })
        self.mapped_field_ids = [(4, created_mapped.id)]

    @api.onchange("model_id")
    def _get_model_name(self):
        if self.model_id.model:
            self.model_name = str(self.model_id.model)

    @api.depends("path", "model_id", "test_item_model_id", "parameter_ids")
    def _compute_path(self):
        for record in self:
            try:
                env_aux = self.env[record.model_id.model].sudo()
                if not record.test_item_model_id or record.test_item_model_id == '' or record.test_item_model_id not in \
                        self.env[record.model_id.model].sudo().search([]).ids:
                    if env_aux.search([]).ids:
                        record.test_item_model_id = env_aux.search([])[0].id

                record.computed_path = record.api_base_url + record.path % tuple(
                    tuple(map(lambda value: env_aux.browse([record.test_item_model_id])[
                        value.field_value.name] if value.type != 'constant' else value.constant_value,
                              record.parameter_ids)))
            except Exception as e:
                record.computed_path = 'Problems with the configuration of request.'

    @api.depends("json_configuration_id", "model_id", "test_item_model_id", "json_pretty")
    def _clean_response(self):
        for record in self:
            record.response_message = ''

    @api.model
    def create(self, values):
        return super().create(values)

    @api.depends("json_configuration_id", "model_id", "test_item_model_id", "json_pretty")
    def _compute_json(self):
        for record in self:
            try:
                env_aux = self.env[record.model_id.model].sudo()
                if record.json_configuration_id and env_aux.browse([record.test_item_model_id]):
                    record.json_example = record.json_configuration_id.get_json(record.json_configuration_id,
                                                                                env_aux.browse(
                                                                                    [record.test_item_model_id]),
                                                                                record.json_pretty)
                else:
                    record.json_example = {}
            except:
                record.json_example = {}

    def action_delete_all_data(self):
        for server in self:
            server.move_ids.unlink()
            server.attachment_ids.unlink()
            server.test_ids.unlink()
            server.application_ids.unlink()
            server.student_ids.unlink()
            server.parent_ids.unlink()
            server.family_ids.unlink()
            server.retrieve_date = False

    def _create_person_facts(self, server, headers):
        self.ensure_one()
        unknown_students = self._send_request(server.computed_path, 'get', headers, '{}')
        students = json.loads(unknown_students.text)['results']
        env_log = self.env['sincro_data_base.log'].sudo()
        log_registers = env_log.search([('url', 'like', 'create_facts')])
        created_students = log_registers.mapped(lambda x: x.item_id);
        new_students = list(filter(lambda x: x['personId'] not in created_students, students))

        if len(new_students) > 0:
            unk_std_id = new_students[0]['personId']
            computed_path = self.api_base_url + '/People/%s' % unk_std_id
            created_res = self._send_request(computed_path, 'put', headers, self.json_example)
            created_log = env_log.create({
                'url': 'create_facts',
                'item_id': unk_std_id,
                'created_date': datetime.now(),
                'status_code': created_res.status_code,
                'request': str(created_res.request.body),
                'response': created_res.text
            })

            return created_res
        else:
            raise ValidationError("No existe usuarios Unknown en FACTS")

    def action_test_connection(self, *args):
        for server in self:
            error_msgs = {}
            headers = {}
            res = False
            for header in server.api_header_ids:
                headers[header.name] = header.value
            res = self._send_request(server.computed_path, server.ws_method, headers, server.json_example)

            server.response_code = res.status_code
            server.response_message = res.text

            env_log = server.env['sincro_data_base.log']
            server.retrieve_date_test = datetime.now()

            created_log = env_log.create({
                'url': server.computed_path,
                'item_id': server.test_item_model_id,
                'created_date': datetime.now(),
                'model': str(server.model_id.model),
                'server_id': server.id,
                'status_code': res.status_code,
                'request': str(server.json_example),
                'response': res.text
            })
            server.log_ids = [(4, created_log.id)]

    def _generate_new_name(self, value, field, model):
        for x in range(MAX_INT):
            new_name = str(value) + ' (%s)' % x
            if not self.env[model].sudo().search([(field, '=', new_name)]):
                return new_name

    def _find_in_list(self, application, list_json, fields_to_check, value, field_return_name):
        if len(list_json) == 0:
            application.write({'status_id': self.env['%s.status' % self.model_id.model].sudo().search(
                [('sequence', '=', application.status_id.sequence - 1)]).id})
            self._cr.commit()
            raise ValidationError("Problems with the connected to FACTS")
        for field in fields_to_check:
            if field not in list_json[0]:
                application.write({'status_id': self.env['%s.status' % self.model_id.model].sudo().search(
                    [('sequence', '=', application.status_id.sequence - 1)]).id})
                self._cr.commit()
                raise ValidationError("A field to checked not exists in the list_json[0]")
        for item in list_json:
            i = 0
            for checked_field in fields_to_check:
                if checked_field in item and str(item[checked_field]) == str(value[checked_field]):
                    i += 1

            if i == len(fields_to_check):
                return item[field_return_name]

        return -1

    # FUNCION QUE COMPRUEBA SI ES False devuelve vacio, el booleano recur determina si es un objeto y comprueba de izquierda a derecha si es vacio para devolver el vacio
    def _clean_false_to_empty(self, value, chain, default_value):
        if not value:
            return default_value
        recur_val = value
        for inner_itm in chain:
            if inner_itm not in recur_val or (inner_itm in recur_val and not recur_val[inner_itm]):
                return default_value
            recur_val = recur_val[inner_itm]

        return recur_val

    def _check_and_create_in_facts(self, check_path, insert_path, headers, json_data):
        res = self._send_request(check_path, 'get', headers, '{}')

        # Si la direccion existe la tomamos del request anterior, de lo contrario la creamos en FACTS
        if 'results' not in json.loads(res.text) or len(json.loads(res.text)['results']) == 0:
            res = self._send_request(insert_path, 'post', headers, json.dumps(json_data))

        return res

    def subscribe(self, order=False, interval_number=False, interval_type=False, nextcall=False):
        for server in self:
            cron_name = 'Cron of sincro_data_base: %s (%s)' % (server.name, server.id)
            if order:
                cron_name = f"{order:02d}. {cron_name}"
            server_cron = server.cron_id
            if not server_cron:
                server_cron_values = {
                    'name': cron_name,
                    'model_id': self.env.ref('sincro_data_base.model_sincro_data_base_server').id,
                    'interval_number': interval_number or server.interval_minutes,
                    'interval_type': interval_type or 'minutes',
                    'numbercall': -1,
                    'state': 'code',
                    'active': False,
                    'code': f"model.browse({server.id}).with_context(email_error=True).action_retrieve_data()"
                }

                if nextcall:
                    server_cron_values['nextcall'] = nextcall
                server_cron = server_cron.create(server_cron_values)
            # creamos la action y la view con la cual se añade  un boton a la vista tipo form
            act_window_env = self.env["ir.actions.act_window"].sudo()
            view_env = self.env["ir.ui.view"].sudo()

            # crear una action para el boton principal el quie crearta los objetos nuevos
            if server.parent_menu_id and not server.parent_menu_item_ids:
                domain = "[('model_id', '=', %s)]" % (
                    server.model_id.id
                )
                vals_action = {
                    "name": _(server.name),
                    "sync_id": '%s_%s.form.sync_from_ws_parent_%s.action' % (
                        server.model_id.model, server.name, server.parent_menu_id.id),
                    "res_model": "sincro_data_base.syncbutton.wizard",
                    "binding_model_id": server.model_id.id,
                    "domain": domain,
                    "target": 'new',
                    "view_mode": 'form',
                }
                parent_act_window_id = act_window_env.create(vals_action)
                vals_menu = {
                    "name": _(server.name),
                    "parent_id": server.parent_menu_id.id,
                    "action": '%s,%s' % ('ir.actions.act_window', parent_act_window_id.id),
                }
                parent_menu_item_id = self.env['ir.ui.menu'].sudo().create(vals_menu)
                parent_act_window_id.write(
                    {'context': '{"server_id": %s,"type":"general_view","model_name":"%s","menu_id":%s}' % (
                        server.id, server.model_id.model, parent_menu_item_id.id)})

            act_window_id = act_window_env.search(
                [('sync_id', '=', '%s.form.sync_from_ws.action' % server.model_id.model)], limit=1)
            if not act_window_id:
                domain = "[('model_id', '=', %s)]" % (
                    server.model_id.id
                )
                vals_action = {
                    "name": _("Sync from WS"),
                    "sync_id": '%s.form.sync_from_ws.action' % server.model_id.model,
                    "res_model": "sincro_data_base.syncbutton.wizard",
                    "binding_model_id": server.model_id.id,
                    "domain": domain,
                    "target": 'new',
                    "view_mode": 'form',
                    "context": '{"server_id": %s}' % server.id,
                }
                act_window_id = act_window_env.create(vals_action)

            view_id = view_env.search([('sync_id', '=', '%s.form.sync_from_ws.view' % server.model_id.model)])
            if not view_id:
                base_view_model_form_id = view_env.search(
                    [('model', '=', server.model_id.model), ('type', '=', 'form'), ('mode', '=', 'primary')],
                    order='priority ASC',
                    limit=1)
                if base_view_model_form_id:
                    arch_base_xml = '<xpath expr="//button[hasclass(\'oe_stat_button\')]" position="before">' \
                                    '<button name="%s"  string="Sync from WS" type="action" class="oe_stat_button" icon="fa-refresh"/>' \
                                    '</xpath>' % act_window_id.id
                    form_xml = \
                        self.env[server.model_id.model].sudo().fields_view_get(base_view_model_form_id.id, 'form')[
                            'arch']

                    if 'oe_stat_button' not in form_xml:
                        arch_base_xml = '<xpath expr="//form/sheet/field" position="before"><div class="oe_button_box" name="button_box">' \
                                        '<button name="%s"  string="Sync from WS" type="action" class="oe_stat_button" icon="fa-refresh"/>' \
                                        '</div></xpath>' % act_window_id.id
                    vals_view = {
                        "name": _("Sync from WS"),
                        "sync_id": '%s.form.sync_from_ws.view' % server.model_id.model,
                        "type": "form",
                        "model": server.model_id.model,
                        "inherit_id": base_view_model_form_id.id,
                        "mode": "extension",
                        "model_data_id": server.model_id.id,
                        "arch_base": arch_base_xml
                    }
                    view_id = view_env.create(vals_view)

            server.write({
                'state': 'subscribed',
                'cron_id': server_cron.id,
                'view_id': view_id,
                'act_window_id': act_window_id.id,
                'parent_act_window_id': server.parent_act_window_id.id if server.parent_act_window_id else False,
                'parent_menu_item_ids': [
                    (6, 0, server.parent_menu_item_ids.ids)] if server.parent_menu_item_ids else False
            })

        return True

    def unsubscribe(self):
        for server in self:
            cron_item = server.cron_id
            if cron_item:
                cron_item.write({'active': False})

            active_server_ids = self.env['sincro_data_base.server'].sudo().search(
                [('state', '=', 'subscribed'), ('model_name', '=', server.model_id.model),
                 ('id', 'not in', server.ids)])

            if not active_server_ids:
                active_server_ids.act_window_id.unlink()
                active_server_ids.parent_act_window_id.unlink()
                active_server_ids.parent_menu_item_id.unlink()
                active_server_ids.parent_menu_item_ids.unlink()

            server.write({"state": "draft"})
        return True


    def _check_conditional_value(self, data, conditional_values):
        for value in conditional_values:
            if (value.json_key not in data) or str(data[value.json_key]).lower() != str(
                    value.conditional_value).lower():
                return False
        return True

    def _check_same_info(self, json_main, json_inner):
        for key, value in json_inner.items():
            if key not in json_main.keys():
                if str(json_inner[key]) not in ['False', '']:
                    return False
                else:
                    continue
            # comprobamos si los 2 son campos booleanos que sean distintos para actualizar
            elif str(json_inner[key]) in ['False', 'True'] and str(json_main[key]) in ['False', 'True'] and str(
                    json_inner[key]) != str(json_main[key]):
                return False
            elif str(json_inner[key]) not in ['False', ''] and str(json_main[key]) != str(json_inner[key]):
                if key in json_main and '[' in str(json_main[key]) and ']' in str(json_main[key]):
                    array_data = list(map(lambda x: str(x), json.loads(str(json_main[key]))))
                    if str(json_inner[key]) not in array_data:
                        return False
                else:
                    return False
        return True

    def _update_cascade_data(self, model_name, active_ids):
        # try:
        for model_id in active_ids:
            model_item = self.env[model_name].sudo().browse(model_id)
            active_server_ids = self.env['sincro_data_base.server'].sudo().search(
                [('state', '=', 'subscribed'), ('model_name', '=', model_name)])
            for server in active_server_ids:
                headers = {}
                for header in server.api_header_ids:
                    headers[header.name] = header.value

                json_keys = {}
                for itm in server.ws_odoo_field_key_ids:
                    if itm.json_key != 'static_value':
                        json_keys[itm.json_key] = model_item[itm.field_id.name]

                server.update_data_ws_odoo(headers, json_keys)

    def split_list(self, alist, wanted_parts=1):
        length = len(alist)
        if not length:
            return []
        return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]

    def _check_data_in_array(self, json_data, json_with_data):
        for idx, itm in json_data.items():
            if itm not in json_with_data[idx]:
                return False
        return True

    def _remove_image_json(self, data):
        image = False
        res_data = {}
        for idx, itm in data.items():
            # es un binario
            if str(itm).startswith('b\''):
                image = itm
            else:
                res_data[idx] = itm

        return res_data, image

    def _run_process(self, webservice_response, conditional_values, env_data_raw, res, update_cascade_fields=True, only_create=False, thread_mode=False):
        self.ensure_one()
        env_log = self.env['sincro_data_base.log'].sudo()
        env_data = self.env[env_data_raw._name].sudo()
        created_items = []
        context = dict(self._context)
        if self.context:
            context = {**context, **safe_eval(self.context)}

        if self.is_active_skip_limit:
            if self.skip > len(webservice_response):
                self.skip = 0

            webservice_response = webservice_response[self.skip:self.skip + self.limit]
            self.skip += self.limit
        _logger.info('Processing update server: %s' % self.name)

        for i, webservice_response_item in enumerate(webservice_response):
            _logger.info('Processing item (server: %s) --> %s/%s' % (self.name, i + 1, len(webservice_response)))
            if not self._check_conditional_value(webservice_response_item, conditional_values):
                continue

            odoo_record_values = False
            active_mapped_fields = self.mapped_field_ids.filtered(lambda mf: mf.is_active and mf.field_id)
            field_name_list = active_mapped_fields.mapped('field_id.name')
            required_field_list = active_mapped_fields.filtered('field_id.required').mapped('field_id.name')

            record_values = self.mapped_field_ids.filtered(lambda mf: mf.is_active and mf.field_id)\
                ._prepare_values_from_response_item(webservice_response_item)

            # comprobamos que existen fields en casacada para actualizarlos antes del propio objeto
            if update_cascade_fields and self.ws_odoo_cascade_key_ids:
                for cascade_field in self.ws_odoo_cascade_key_ids:
                    if str(cascade_field.field_id.name) in record_values:
                        self._update_cascade_data(cascade_field.key_field_id.model_id.model,
                                                        [record_values[cascade_field.field_id.name]])

            json_keys = []
            if self.include_archived and 'active' in env_data._fields:
                json_keys.append(('active', 'in', [False, True]))

            for itm in self.ws_odoo_field_key_ids:
                # mapped_field.json_key
                if not itm.field_id or itm.field_id.name not in record_values:
                    _logger.warning("Item %s has empty field_id" % itm.name_get()[0][1])
                    continue
                data_item_aux = record_values[itm.field_id.name]
                # vamos a tomar el valor por defecto si es el bvalor estatico en el campo para poder condificonar con este valor si se requiere como en elk caso que queremos que solo afecvte a indominio predeterminado en el sistema.
                if itm.json_key == 'static_value':
                    data_item_aux = itm.default_value

                json_keys.append((itm.field_id.name,
                                    'in' if itm.field_id.ttype in ['many2many', 'one2many'] else '=',
                                    [data_item_aux] if itm.field_id.ttype in ['many2many',
                                                                            'one2many'] else
                                    data_item_aux))

            existed_item = env_data.with_context(context).search(json_keys, limit=1)
            # compruebo que el external id existe para actualizar de lo contrario inserto
            if existed_item:
                # compruebo que en la configuracion solo indique que solo se puede crear
                if self.only_create_item:
                    continue
                # odoo_record_values = self.mapped_field_ids.filtered('is_active')._prepare_values_from_response_item(existed_item)
                odoo_record_values = existed_item.read(field_name_list, load='_eduweb_dict_read')[0]

                if not self._check_same_info(odoo_record_values, record_values):
                    # guardo los ids sin darle el formato para el write, asi es mas facil la comprobacion con el array y los ids.
                    ids_for_checking = {}
                    # damos el formato correcto a los campos con tipo one2many or many2many
                    for mapped_field in self.mapped_field_ids.filtered(lambda x: x.field_id):
                        if mapped_field.field_id.ttype in ['many2many', 'one2many']:
                            if not int(record_values[mapped_field.field_id.name]):
                                record_values.pop(mapped_field.field_id.name, None)
                            # se forzara la sobreescritura del campo
                            elif mapped_field.force_overwrite:
                                record_values[mapped_field.field_id.name] = [
                                    (6, 0, [int(record_values[mapped_field.field_id.name])])]
                            # solo se añadira otra info mas
                            else:
                                record_values[mapped_field.field_id.name] = [
                                    (4, int(record_values[mapped_field.field_id.name]))]
                        elif mapped_field.field_id.ttype == 'selection':
                            value_aux = record_values[mapped_field.field_id.name]
                            options = mapped_field.field_id.selection_ids.mapped(lambda x: x.value)
                            if len(list(filter(lambda x: x.lower() == value_aux.lower(), options))) > 0:
                                record_values[mapped_field.field_id.name] = \
                                    list(filter(lambda x: x.lower() == value_aux.lower(), options))[0]
                            else:
                                if mapped_field.default_value:
                                    record_values[mapped_field.field_id.name] = mapped_field.default_value
                                else:
                                    record_values[mapped_field.field_id.name] = False
                    skip_record = False
                    for required_field in required_field_list:
                        if required_field in record_values and not record_values[required_field]:
                            _logger.warning(f"Required field {required_field} for {self.name} server({self.id}) is not set record updating for model: {env_data._name}")
                            skip_record = True
                            break
                    if skip_record:
                        continue
                    existed_item.write(record_values)
                    existed_item._cr.commit()
                else:
                    continue
            # inserto nuevo registro
            else:
                # si solo esta configurado para actualizar cuando no lo encuentro por la clave debo salir
                if self.only_update:
                    continue

                is_required_empty = False
                for mapped_field in self.mapped_field_ids.filtered(lambda x: x.field_id):
                    if mapped_field.field_id.required and (
                            mapped_field.field_id.name not in record_values or not record_values[
                        mapped_field.field_id.name]):
                        is_required_empty = True
                        continue

                    if mapped_field.field_id.ttype in ['many2many', 'one2many']:
                        if not int(record_values[mapped_field.field_id.name]):
                            record_values.pop(mapped_field.field_id.name, None)
                        # se forzara la sobreescritura del campo
                        elif mapped_field.force_overwrite:
                            record_values[mapped_field.field_id.name] = [
                                (6, 0, [int(record_values[mapped_field.field_id.name])])]
                        # solo se añadira otra info mas
                        else:
                            record_values[mapped_field.field_id.name] = [
                                (4, int(record_values[mapped_field.field_id.name]))]
                    elif mapped_field.field_id.ttype == 'selection':
                        value_aux = record_values[mapped_field.field_id.name]
                        options = mapped_field.field_id.selection_ids.mapped(lambda x: x.value)
                        if len(list(filter(lambda x: x.lower() == value_aux.lower(), options))) > 0:
                            record_values[mapped_field.field_id.name] = \
                                list(filter(lambda x: x.lower() == value_aux.lower(), options))[0]
                        else:
                            if mapped_field.default_value:
                                record_values[mapped_field.field_id.name] = mapped_field.default_value
                            else:
                                record_values[mapped_field.field_id.name] = False

                if is_required_empty:
                    continue

                # si esta creandolo desde el boton de la vista, guardara en un system default field un json con los datos insertados para que de esta manera, los que se encargan de actualizar la información sepan que se han creado recientemente y se actualizen
                for required_field in required_field_list:
                    if not record_values.get(required_field, False):
                        _logger.warning(f"Required field {required_field} for {self.name} server({self.id}) is not set record creation for model: {env_data._name}")
                        continue

                item_id = env_data.create(record_values)
                env_data._cr.commit()
                created_items.append(record_values)
            # remuevo los campos de imagen, ya que daba errorfes por archiuvos binarios tan largos
            record_values, new_image_bin = self._remove_image_json(record_values)

            data_log = {
                'url': 'New register' if not existed_item else 'Update Register',
                'item_id': existed_item.id or item_id.id or False,
                'created_date': datetime.now(),
                'model': str(self.model_id.model),
                'server_id': self.id,
                'new_value': str(record_values),
                'new_image': new_image_bin

            }
            if odoo_record_values:
                odoo_record_values, old_image_bin = self._remove_image_json(odoo_record_values)
                data_log['old_value'] = str(odoo_record_values) or False
                data_log['old_image'] = old_image_bin

            if existed_item or item_id and self.is_save_in_log:
                created_log = env_log.create(data_log)

            self.log_ids = [(4, created_log.id)]

        return created_items

    def update_data_ws_odoo(self, headers, json_keys_from_views=False, only_create=False, new_items=[]):
        for server in self:
            self.ensure_one()
            context = dict(self._context)
            if server.context:
                context = {**context, **safe_eval(server.context)}
            res = self._send_request(server.computed_path, server.ws_method, headers, '{}')
            if res.status_code != 200:
                raise ValidationError(_("Some error during api request: status code: %s, message:\n%s", res.status_code, res.text))
            webservice_response = res.json()
            if server.key_json_data and server.key_json_data in webservice_response:
                webservice_response = webservice_response[server.key_json_data]

            conditional_values = server.mapped_field_ids.filtered(lambda x: x.conditional_value)
            env_data = self.env[server.model_id.model].sudo()
            if only_create:
                key_data_json = []
                domain_array = []
                for key in server.ws_odoo_field_key_ids.filtered(lambda x: x.json_key == 'static_value'):
                    domain_array.append((key.field_id.name, '=', str(key.default_value)))

                create_items = self.env[server.model_id.model].with_context(context).sudo().search(domain_array)
                filtered_data = []
                key_not_statics = server.ws_odoo_field_key_ids.filtered(lambda x: x.json_key != 'static_value')
                key_create_data = {}

                for key_aux in key_not_statics:
                    key_create_data[key_aux.field_id.name] = list(
                        map(lambda x: x[key_aux.field_id.name].id if isinstance(x[key_aux.field_id.name],
                                                                                odoo.models.Model) else x[
                            key_aux.field_id.name],
                            create_items.filtered(lambda y: y[key_aux.field_id.name])))
                    if len(list(filter(lambda x: key_aux.field_id.name in x, new_items))):
                        data_new_items = list(map(lambda y: y[key_aux.field_id.name],
                                                  filter(lambda x: key_aux.field_id.name in x, new_items)))
                        key_create_data[key_aux.field_id.name] = [data for data in
                                                                  key_create_data[key_aux.field_id.name] if
                                                                  str(data) not in data_new_items]

                for itm_data in webservice_response:
                    check = True
                    idx = 0
                    while check and idx < len(key_not_statics):
                        if key_not_statics[idx].json_key not in itm_data or str(
                                itm_data[key_not_statics[idx].json_key]) in \
                                key_create_data[key_not_statics[idx].field_id.name]:
                            check = False
                        idx += 1
                    if check:
                        filtered_data.append(itm_data)

                webservice_response = filtered_data

            elif not only_create and json_keys_from_views:
                filtered_data = list(filter(lambda x: self._check_same_info(x, json_keys_from_views), webservice_response))
                webservice_response = filtered_data

            server.total_request = len(webservice_response)
            return server._run_process(webservice_response, conditional_values, env_data, res, True if json_keys_from_views else False, only_create)

    # queda desarrollar esta parte
    def update_data_odoo_ws(self, headers):
        for server in self:
            self.ensure_one()

    def action_retrieve_data(self, *args):
        
        _logger.info("action_retrieve_data function")
        pass
        # env_id = self.env['ir.model'].sudo().search([('model', '=', 'sincro_data_base.server')]).id
        # for server in self:
        #     self.ensure_one()
        #     error_msgs = {}
        #     headers = {}
        #     for header in server.api_header_ids:
        #         headers[header.name] = header.value

        #     if server.method == 'ws_odoo':
        #         return self.update_data_ws_odoo(headers)

        #     if server.method == 'odoo_ws':
        #         return self.update_data_ws_odoo(headers)

        #     aux_domain = safe_eval(server.domain or "[]")
        #     env_aux = server.env[server.model_id.model]

        #     filtered_items = env_aux.search(aux_domain)

        #     for item in filtered_items:
        #         computed_path = server.api_base_url + server.path % tuple(
        #             reversed(tuple(map(lambda value: env_aux.browse([item.id])[
        #                 value.field_value.name] if value.type != 'constant' else value.constant_value,
        #                                server.parameter_ids))))

        #         compute_json_data = server.json_configuration_id.get_json(server.json_configuration_id,
        #                                                                   env_aux.browse(
        #                                                                       [item.id]),
        #                                                                   server.json_pretty)

        #         res = server._send_request(computed_path, server.ws_method, headers, compute_json_data)

        #         env_log = server.env['sincro_data_base.log']
        #         created_log = env_log.create({
        #             'url': computed_path,
        #             'item_id': item.id,
        #             'created_date': datetime.now(),
        #             'model': str(env_id),
        #             'status_code': res.status_code,
        #             'server_id': self.id,
        #             'request': str(res.request.body),
        #             'response': res.text
        #         })
        #         self.log_ids = [(4, created_log.id)]

        #     server.retrieve_date = datetime.now()

    def _send_request(self, url, method, headers, body):
        self.ensure_one()
        return requests.request(method, url, headers=headers, json=json.loads(body))

    def _save_in_log(self, server, url, created_date, server_id, model='', item_id=-1, status_code='', request='',
                     response='', method=''):
        env_log = self.env['sincro_data_base.log'].sudo()
        server.retrieve_date = datetime.now()
        created_log = env_log.create({
            'url': url,
            'item_id': item_id,
            'created_date': created_date,
            'model': str(model),
            'method': method,
            'server_id': server_id,
            'status_code': status_code,
            'request': str(request),
            'response': str(response)
        })
        self.log_ids = [(4, created_log.id)]
