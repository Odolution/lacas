import requests
import json
from odoo.exceptions import UserError
from odoo import models, fields, api, exceptions


class Token_Credential(models.Model):
    _name = "api.users"

    name=fields.Char(string="Name",required=True)
    username=fields.Char(string="Username ")
    password=fields.Char(string="Password")
    token=fields.Char(string="Token")
    token_expiry=fields.Date(string="Token Expire:")
    token_refresh=fields.Char(string="Token Refresh")

