# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests


class HttpUtils(models.AbstractModel):
    _name = 'edoob.facts.http.utils'

    @api.model
    def _send_facts_api_request(self, url):
        ConfigParam = self.env['ir.config_parameter'].sudo()
        subscription_key = ConfigParam.get_param('school_facts.subscription_key')
        api_key = ConfigParam.get_param('school_facts.facts_api_key')

        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Facts-Api-Key': api_key
            }
        facts_response = requests.get(url, headers=headers)
        return facts_response

    @api.model
    def _send_eduweb_api_request(self, url):
        ConfigParam = self.env['ir.config_parameter'].sudo()
        eduweb_api_key = ConfigParam.get_param('school_facts.eduweb_api_key')

        headers = {
            'api-key': eduweb_api_key
            }
        eduweb_response = requests.get(url, headers=headers)
        return eduweb_response
