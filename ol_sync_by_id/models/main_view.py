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
            school = self.env['school.school'].search(['name','=',data['Current School']])
            grade = self.env['school.grade.level'].search(['name','=',data['Current_Enrolled']])
            raise UserError(data)
            if data:
                rec['name']=data["Name"]
                rec['street']=data['Address']
                rec['date_of_birth']=data['Date Of Birth']
                rec['facts_udid']=data['udid']
                rec['email'] = data['Email']
                rec['phone'] = data['Phone']
                rec['school_ids'] = school.id
                rec['grade_level_ids'] = grade.id
                rec['homeroom'] = data['Homeroom']
                                                           
                                                    
                
                
