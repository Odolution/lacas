from re import U
import string

from odoo import models, fields,api
from odoo.exceptions import UserError
import base64
import requests
import datetime


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
                    schoo_name = data['Current School']
                    school = self.env['school.school'].search([])
                    for i in school:
                        if i.name == schoo_name:
                            rec['school_ids'] = i
                
            if  'grade_level' in data:
                if data['grade_level']:
                    grade_name = data['grade_level']
                    grade = self.env['school.grade.level'].search([])
                    for j in grade:
                        if j.name == grade_name:
                            rec['grade_level_ids'] = j
               
            if 'Current_Enrolled' in data:
                enrol = data['Current_Enrolled']
                enroled = self.env['school.enrollment.status'].search([])
                for k in enroled:
                    if enrol == k.name:
                        if enrol == "Graduate":
                            rec['grade_level_ids'] = False
                            rec['enrollment_status_ids'] = k
                            
                        else:
                            rec['enrollment_status_ids'] = k
            
            if  'Homeroom' in data:
                rec['homeroom'] = data['Homeroom']
            
            
            if data:
                rec['name']=data["Name"]
                rec['street']=data['Address']
                rec['date_of_birth'] = data['Date Of Birth']
                rec['facts_udid']=data['udid']
                rec['email'] = data['Email'] 
                rec['phone'] = data['Phone']
                 
                                                           
                                                    
                
                
