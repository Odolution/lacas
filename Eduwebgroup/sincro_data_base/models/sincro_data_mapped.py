# -*- coding:utf-8 -*-
import base64
import datetime

import requests

from odoo import models, fields, api
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import logging

_logger = logging.getLogger(__name__)

class SincroDataMapped(models.Model):
    _name = "sincro_data_base.mapped"
    _description = "Sincro Data Mapped"

    json_key = fields.Char("JSON key")
    field_id = fields.Many2one('ir.model.fields', string='Model field', store=True)
    related_model_name = fields.Char(related='field_id.relation', readonly=True)
    key_field_id = fields.Many2one('ir.model.fields', string='Model field Key', store=True)
    server_id = fields.Many2one("sincro_data_base.server", readonly=True)
    model_id = fields.Many2one("ir.model", string="Model", readonly=True, related="server_id.model_id")
    conditional_value = fields.Char(string="Conditional value")
    concat_value = fields.Char(string="Contact value")
    default_value = fields.Char(string="Default value")
    is_active = fields.Boolean("Sincronize", default=True)
    is_force_create = fields.Boolean("Force created", default=False)
    force_overwrite = fields.Boolean("Force Overwrite", default=True)
    is_an_img_from_url = fields.Boolean("URL Img", default=False)
    is_default = fields.Boolean("Field by default", default=True)
    is_field_required = fields.Boolean(related="field_id.required")
    field_domain = fields.Char(string="Domain")
    letter_case = fields.Selection(selection=[
        ('default', "Default"),
        ('lower', "Lowercase"),
        ('upper', "Uppercase"),
        ], string="Letter case", required=True, default='default')

    def name_get(self):
        return [(record.id, '%s (%s)' % (record.json_key, record.field_id.name or '')) for record in self]

    @api.onchange("is_active")
    def _reset_booleans(self):
        for record in self:
            if not record.is_active:
                record.is_force_create = False
                record.force_overwrite = False
                record.is_an_img_from_url = False

    @api.model
    def _get_proper_formatted_data_for_field_from_dict(self, value, path, field_type):
        aux_value = value
        for level in path:
            if level in aux_value:
                aux_value = aux_value[level]
            else:
                aux_value = ''

        if isinstance(aux_value, models.Model):
            if field_type not in ['many2one', 'many2many']:
                aux_value = aux_value.ids[0] if aux_value else False
            else:
                aux_value = aux_value.ids
        if not aux_value:
            return False

        if field_type in ['date', 'datetime']:
            if isinstance(aux_value, int):
                # aux_value = datetime.datetime.fromtimestamp(aux_value).strftime(DEFAULT_SERVER_DATE_FORMAT)
                aux_date = datetime.datetime.fromtimestamp(aux_value)
            else:
                aux_value = aux_value.replace('T', ' ').replace('Z', '')
                aux_date = fields.Datetime.from_string(aux_value)
                aux_value = aux_date.strftime(DEFAULT_SERVER_DATE_FORMAT) if field_type == 'date' else aux_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        elif field_type == 'boolean':
            aux_value = str(aux_value).lower() in ('true', '1')
        return aux_value

    def _prepare_values_from_response_item(self, response_item):
        res = {}
        # tomo solo los fields que tengan un field_id asociado
        server = self.mapped('server_id')
        if len(server) > 1:
            raise ValidationError(_("Using multiple mapped_fields from different servers"))
        odoo_model = isinstance(response_item, models.Model)
        for mapped_field in self:
            context = dict(self._context)
            if mapped_field.server_id.context:
                context = {**context, **safe_eval(mapped_field.server_id.context)}
            if mapped_field.is_active:
                mapped_field_data = mapped_field.json_key
                field_type = mapped_field.field_id.ttype

                if mapped_field.key_field_id:
                    if mapped_field_data == 'static_value' and not odoo_model:
                        domain = [(mapped_field.key_field_id.name, '=', mapped_field.default_value)]
                        if mapped_field.field_domain:
                            aux_domain = safe_eval(mapped_field.field_domain or "[]", globals_dict=response_item)
                            domain = expression.AND([domain, aux_domain])
                        res[mapped_field.field_id.name] = self.env[mapped_field.related_model_name].sudo().with_context(context).search(domain).id
                    else:
                        aux_value = self._get_proper_formatted_data_for_field_from_dict(response_item, mapped_field_data.split('/'), field_type)
                        if aux_value:

                            if type(aux_value) == str and mapped_field.letter_case != 'default':
                                if mapped_field.letter_case == 'lower':
                                    aux_value = aux_value.lower()
                                elif mapped_field.letter_case == 'upper':
                                    aux_value = aux_value.upper()

                            key_field_name = mapped_field.key_field_id.name

                            if odoo_model and str(field_type) in ['many2one', 'many2many', 'one2many']:
                                key_field_name = 'id'
                            many2many_or_many2one = mapped_field.field_id.ttype in ['many2one', 'many2many'] and odoo_model
                            aux_domain = [(key_field_name, '=' if not many2many_or_many2one else 'in', aux_value)]

                            if mapped_field.field_domain:
                                aux_domain += safe_eval(mapped_field.field_domain or "[]", globals_dict=response_item)
                            aux_data = self.env[mapped_field.related_model_name].with_context(context).sudo().search(aux_domain)

                            if not many2many_or_many2one:
                                res[mapped_field.field_id.name] = aux_data.ids[0] if len(aux_data.ids) > 0 else False
                            else:
                                res[mapped_field.field_id.name] = aux_data.ids if aux_data else False

                            if not res[mapped_field.field_id.name] and mapped_field.default_value and not odoo_model:
                                res[mapped_field.field_id.name] = int(mapped_field.default_value)
                        elif mapped_field.force_overwrite:
                            res[mapped_field.field_id.name] = False
                        elif mapped_field.default_value:
                            res[mapped_field.field_id.name] = int(mapped_field.default_value)
                else:
                    if mapped_field_data == 'static_value':
                        res[mapped_field.field_id.name] = mapped_field.default_value
                    else:
                        aux_val = res[mapped_field.field_id.name] = self._get_proper_formatted_data_for_field_from_dict(response_item, mapped_field_data.split('.'), field_type)

                        if type(aux_val) == str and mapped_field.letter_case != 'default':
                            if mapped_field.letter_case == 'lower':
                                aux_val = aux_val.lower()
                            elif mapped_field.letter_case == 'upper':
                                aux_val = aux_val.upper()
                        if not odoo_model:
                            if mapped_field.is_an_img_from_url and aux_val:
                                try:
                                    if mapped_field.concat_value:
                                        aux_val = mapped_field.concat_value % aux_val
                                    rq = requests.get(str(aux_val).strip())
                                    _logger.info('aux_val: %s' % str(aux_val))
                                    _logger.info('rq.content: %s' % str(rq))
                                    if rq.status_code != 200:
                                        # check default value
                                        if mapped_field.default_value:
                                            default_rq = requests.get(str(mapped_field.default_value).strip())
                                            if default_rq.status_code == 200:
                                                res[mapped_field.field_id.name] = base64.b64encode(default_rq.content).replace(b'\n', b'')
                                            else:
                                                res[mapped_field.field_id.name] = False
                                        else:
                                            res[mapped_field.field_id.name] = False
                                    else:
                                        res[mapped_field.field_id.name] = base64.b64encode(rq.content).replace(b'\n', b'')
                                except Exception as e:
                                    _logger.error(e)
                                    res[mapped_field.field_id.name] = False
                            else:
                                res[mapped_field.field_id.name] = aux_val

                    if not res[mapped_field.field_id.name] and mapped_field.default_value and not odoo_model:
                        res[mapped_field.field_id.name] = mapped_field.default_value
                if mapped_field.field_id.name and mapped_field.field_id.name == 'email':
                    res['email'] = str(res['email']).replace('ñ', 'n')
        return res
