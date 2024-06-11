# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.exceptions import MissingError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def _get_sincro_log(self):
        return "ASD"

    def _read_format(self, fnames, load='_classic_read'):
        if load != '_eduweb_dict_read':
            return super()._read_format(fnames, load)
        data = [(record, {'id': record._ids[0]}) for record in self]
        for name in fnames:
            field = self._fields[name]
            if field.type in ['datetime', 'date']:
                def convert(value, record, use_name_get=False):
                    if not value:
                        return False
                    date_value = field.convert_to_read(value, record, use_name_get)
                    if field.type == 'datetime':
                        return date_value.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    elif field.type == 'date':
                        return date_value.strftime(DEFAULT_SERVER_DATE_FORMAT)
            else:
                convert = field.convert_to_read
            for record, vals in data:
                if not vals:
                    continue
                try:
                    vals[name] = convert(record[name], record, use_name_get=False)
                except MissingError:
                    vals.clear()
        result = [vals for record, vals in data if vals]
        return result

