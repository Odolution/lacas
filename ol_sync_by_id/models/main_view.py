import datetime
from re import U
import string

from odoo import models, fields,api
from odoo.exceptions import UserError
import base64
import requests
from datetime import datetime, timedelta


class RespartnerInherit(models.Model):
    _inherit = 'school.student'
    
    def sync_wd_facts(self):
        for rec in self:
            x = requests.get('http://97.74.85.51:5631/facts/'+str(rec.facts_id))
            data=x.json()
            data = eval(data)
            if data:
                add_data={
                    'name':data["Name"],
                    'street':data["Address"],
                    'email':data["Email"],
                    'phone':data["Phone"],
                    'homeroom':data["Current_Enrolled"]
                }
                rec.write(add_data)
