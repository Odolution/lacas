from re import U
import string

from odoo import models, fields,api
from odoo.exceptions import UserError
import base64
import requests
import datetime
from ..fact_api.factapi import Fact_Api

class RespartnerInherit(models.Model):
    _inherit = 'res.partner'
    
    def sync_wd_facts(self,std):
        
        for rec in std:
            
            fact_obj = Fact_Api()
            fact_data = fact_obj.main(rec.facts_id)
            student = fact_data['student']
            pickup = fact_data['pickup']
            people = fact_data['people']
            personfamily = fact_data['personfamily']
            family = fact_data['family']
            demographic = fact_data['demographic']

            school = self.env['school.school'].search([('code','=',student['schoolCode'])])
            if school:
                rec['school_ids'] = school
            
            #grade level
            for line in rec['enrollment_state_ids']:
                grade_obj = self.env['school.grade.level'].search([('name','=',student['school']['gradeLevel'])])
                for i in grade_obj:
                    line['grade_level_id'] = i.id
                

                next_grade_obj = self.env['school.grade.level'].search([('name','=',student['school']['nextGradeLevel'])])
                for i in next_grade_obj:
                    line['next_grade_level_id'] = i.id
                
                
                enrol_status_obj = self.env['school.enrollment.status'].search(['name','=',student['school']['status']])
                raise UserError(str(enrol_status_obj))
                # for i in enrol_status_obj: 
                #     line['enrollment_status_id'] = i.id
                
                # next_enrol_status_obj = self.env['school.enrollment.status'].search(['name','=',student['school']['nextStatus']])
                # for i in next_enrol_status_obj:
                #     line['next_enrollment_status_id'] = i.id



            
            # x = requests.get('http://209.145.61.122:5631/facts/'+str(rec.facts_id))
            # data=x.json()
            
            # data = eval(data)
            
            
            # sch_id = False
            # grd_id = False
            # if 'Current School' in data:
            #     if data['Current School']:
            #         schoo_name = data['Current School']
            #         school = self.env['school.school'].search([])
            #         for i in school:
            #             if i.name == schoo_name:
            #                 rec['school_ids'] = i
                
               
            # if 'Current_Enrolled' in data:
            #     enrol = data['Current_Enrolled']  
            #     enroled = self.env['school.enrollment.status'].search([])
            #     for k in enroled:
            #         if enrol == k.name:
            #             if enrol == "Graduate":
            #                 rec['grade_level_ids'] = False
            #                 rec['enrollment_status_ids'] = k
                            
            #             else:
            #                 rec['enrollment_status_ids'] = k
            #                 if  'grade_level' in data:
            #                     if data['grade_level']:
            #                         grade_name = data['grade_level']
            #                         grade = self.env['school.grade.level'].search([])
            #                         for j in grade:
            #                             if j.name == grade_name:
            #                                 rec['grade_level_ids'] = j
            
            
            # if  'Homeroom' in data:
            #     rec['homeroom'] = data['Homeroom']
            
            
            # if data:
            #     rec['name']=data["Name"]
            #     rec['street']=data['Address']
            #     rec['date_of_birth'] = data['Date Of Birth']
            #     rec['facts_udid']=data['udid']
            #     rec['email'] = data['Email'] 
            #     rec['phone'] = data['Phone'] 
                  
                                                           
                                                    
                
                
