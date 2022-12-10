import datetime
from re import U
import string

from odoo import models, fields,api
from odoo.exceptions import UserError
import base64
import requests
from datetime import datetime, timedelta


class RespartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    def sync_wd_facts(self,std):
        for rec in std:
            x = requests.get('http://97.74.85.51:5631/facts/'+str(rec.facts_id))
            
            data=x.json()
            
            data = eval(data)
            if data:
                rec['name']=data["Name"]
