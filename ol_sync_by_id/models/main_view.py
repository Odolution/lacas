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
        school_name_key = {
                "LACAS Burki A Level":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Es1KXmdfd3HW/L5pUdC5wIN/yE5ZQvnMbka3pPqvH0sig4fZrSKriKgsA1QPjsfJSU=",
                "LACAS Burki Boys":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvlFxL8JZDP8b8yHRK/zLqt00IjeqpiNMsinE6yLyZbpp0itPr5auIhwYsRcAWgS2Y=",
                "LACAS Burki Girls":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvXkvotYZrCGtco1K5xitUYFWwQOEH0YZZk9M6eEKA3aUI5f8pVNjnOUaK80r0c0l4=",
                "LACAS Burki Pre-School":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvggvbAqbkN9REut7igY3Q46gqBotTnxmEIwF83Mx3GyuLstDwvhZS9WEvYRZ1wyc4=",
                "LACAS Canal Side Girls":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuJN4Zyo/mySix0w5jItTKTqYuxRVyqrIHu0npfdrAVESAcNfiq2rKSdwa4TRg4pR0=",
                "LACAS DHA Islamabad":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EtfA3ffT3JqLDDzAGj4zitoMiRzc6uyA/CLZoeHk8K+G3lOG2tJLp1fcCNUyL34HPI=",
                "LACAS Gujranwala Boys":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuxRKdVGo7v/fF5et+i4pfpdsli1s1Xpz/0RpoPavfOBAuYQUCiGVv+JZkbNb2u9pA=",
                "LACAS Gujranwala Girls":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuFP+ahrehuubNGKr+ZQ2CVPGYPHkanVtwi+liVomCq2jrSdFbyiKQ3qIOxTfyge2s=",
            }    
        for rec in std:
            
            
            fact_obj = Fact_Api()
            
            school_name = school_name_key[str(rec.school_ids.name)]
            fact_data = fact_obj.main(rec.facts_id,school_name)
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
                
                
                enrol_status_obj = self.env['school.enrollment.status'].search([])
                for i in enrol_status_obj: 
                    if str(i.name) == str(student['school']['status']):
                        line['enrollment_status_id'] = i.id
                    if str(i.name) == str(student['school']['nextStatus']):
                        line['next_enrollment_status_id'] = i.id

            first_name = people['firstName']
            last_name = people['lastName']
            email = people['email']
            phone = people['homePhone']
            mobile = people['cellPhone']
            gender = demographic['gender']
            birthdate = demographic['birthdate']

            rec['first_name'] = first_name
            rec['last_name'] = last_name
            rec['email'] = email
            rec['phone'] = phone
            rec['mobile'] = mobile
            rec['date_of_birth'] = birthdate
            rec['gender'] = gender 


            
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
                  
                                                           
                                                    
                
                
