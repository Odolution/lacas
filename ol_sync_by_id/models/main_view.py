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
            
            x = requests.get('http://209.145.61.122:5631/facts/'+str(rec.facts_id))
            data=x.json()
            
            data = eval(data)
            gradelvl = self.env['school.grade.level'].search([])
            if 'Current School' in data:
                if data['Current School']:
                    schoo_name = data['Current School']
                    school = self.env['school.school'].search([])
                    for i in school:
                        if i.name == schoo_name:
                            rec['school_ids'] = i
                
            enroled = self.env['school.enrollment.status'].search([])   
            if 'Current_Enrolled' in data:
                enrol = data['Current_Enrolled']  
                
                for k in enroled:
                    if str(enrol) == "Withdrawn" or str(enrol) == "Graduate":
                        if str(enrol) == str(k.name):
                            rec['enrollment_status_ids'] = k
                            rec['grade_level_ids'] = False
                            for next_line in rec.enrollment_state_ids:
                                next_line.enrollment_status_id = k.id
                                next_line.grade_level_id = False
                                next_line.next_grade_level_id = False
                                next_line.next_enrollment_status_id = False
                       
                    if str(enrol) == "Admissions":
                        if str(enrol) == str(k.name):
                            
                            rec['enrollment_status_ids'] = k
                            rec['grade_level_ids'] = False
#                             nxt_status = self.env['school.enrollment.status'].search([])
#                             for next_line in rec.enrollment_state_ids:
#                                 Next_Enrolled = data['Next_Enrolled']
#                                 for f in nxt_status:
#                                     if str(Next_Enrolled) == str(f.name):
#                                         nxt = data['nxt_grade']
#                                         for nxtgrd in gradelvl:
#                                             if str(nxt) == str(nxtgrd.name):
#                                                 next_line.grade_level_id = False
#                                                 next_line.next_grade_level_id = nxtgrd.id
#                                                 next_line.next_enrollment_status_id = f.id


                                                
                    if str(enrol) == "Enrolled":
                        if str(enrol) == str(k.name):
                            rec['enrollment_status_ids'] = k
                            if  'grade_level' in data:
                                if data['grade_level']:
                                    grade_name = data['grade_level']
                                    for j in gradelvl:
                                        if j.name == grade_name:
                                            rec['grade_level_ids'] = j
#                                             for ngrade_rec in rec.enrollment_state_ids:
#                                                 ngrade_rec.grade_level_id = j.id
#                                                 ngrade_rec.next_enrollment_status_id = k.id
#                                         if data['nxt_grade']:
#                                             nxt_grade = data['nxt_grade']
#                                             for ngrade_rec in rec.enrollment_state_ids:
#                                                 if j.name == nxt_grade:
#                                                     ngrade_rec.next_grade_level_id = j.id
#                                                 if data['Next_Enrolled'] == k.name:
#                                                     ngrade_rec.next_enrollment_status_id = k.id

                                        
                                                
                                                

                                        
                                        
                                    
                              
                              
                            
            
           
                                    
                                        
            
            
            if  'Homeroom' in data:
                rec['homeroom'] = data['Homeroom']
            
            
            if data:
                rec['name']=data["Name"]
                rec['street']=data['Address']
                rec['date_of_birth'] = data['Date Of Birth']
                rec['facts_udid']=data['udid']
                rec['email'] = data['Email'] 
                rec['phone'] = data['Phone'] 
                  
                                                           
                                                    
                
                
