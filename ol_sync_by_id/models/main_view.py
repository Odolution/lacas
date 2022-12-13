from re import U
import string

from odoo import models, fields,api
from odoo.exceptions import UserError
import base64
import requests
from datetime import datetime


class RespartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    def sync_wd_facts(self,std):
        for rec in std:
            x = requests.get('http://97.74.85.51:5631/facts/'+str(rec.facts_id))
            
            data=x.json()
            
            data = eval(data)
            
            sch_id = False
            grd_id = False
            if 'Current School' in data:
                if data['Current School']:
                    school = self.env['school.school'].search(['name','=',data['Current School']])
                    rec['school_ids'] = school.id
                
            if  'Current_Enrolled' in data:
                if data['Current_Enrolled']:
                    grade = self.env['school.grade.level'].search(['name','=',data['Current_Enrolled']])
                    rec['grade_level_ids'] = grade.id
               
               
            
            
            if data:
                rec['name']=data["Name"]
                rec['street']=data['Address']
                rec['date_of_birth'] = datetime.datetime.strptime(data['Date Of Birth'], '%m/%d/%Y')
                rec['facts_udid']=data['udid']
                rec['email'] = data['Email']
                rec['phone'] = data['Phone']
                rec['homeroom'] = data['Homeroom']
                                                           
                                                    
                
                
