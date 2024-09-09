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
                "LACAS Burki Preschool":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvggvbAqbkN9REut7igY3Q46gqBotTnxmEIwF83Mx3GyuLstDwvhZS9WEvYRZ1wyc4=",
                "LACAS Canal Side Girls":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuJN4Zyo/mySix0w5jItTKTqYuxRVyqrIHu0npfdrAVESAcNfiq2rKSdwa4TRg4pR0=",
                "LACAS DHA Islamabad":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EtfA3ffT3JqLDDzAGj4zitoMiRzc6uyA/CLZoeHk8K+G3lOG2tJLp1fcCNUyL34HPI=",
                "LACAS Gujranwala Boys":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuxRKdVGo7v/fF5et+i4pfpdsli1s1Xpz/0RpoPavfOBAuYQUCiGVv+JZkbNb2u9pA=",
                "LACAS Gujranwala Girls":"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuFP+ahrehuubNGKr+ZQ2CVPGYPHkanVtwi+liVomCq2jrSdFbyiKQ3qIOxTfyge2s=",
                'LACAS Gujranwala Preschool':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvXUmtSx7BRoLlFWJSC+S8UvPfeJTrRKf1B39SqgL9IFgZPDgHuERPKNSTbvcs4zyU=",
                'LACAS Gulberg Boys':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Eu7ZF0G/G+uhCWsREBymtiJW5tlVEPOaSDctrmMwWl2dWWP2L/6LFM2wsKjVFs5sKA=",
                'LACAS Gulberg Girls Campus':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Ev7yLv6RExMMdkIaqTCFdkEj+tLcR6vZTEsdzErN/3YOonsMlHpBVAhZpDu0QmShX0=",
                'LACAS Johar Town A Level':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EsfOTcUgpx0G1h3KDph3Q9FuXveh9gFPVh1+T5qHM7nNrwOwNqZeYM+hA3LOGjQWpU=",
                'LACAS Johar Town Boys':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Ev2cn6iSZy5hGxz4wTMwVXGLYm033yS0nqW32u2tNgR86Q3qkjoJw0UMd9QL/1qZA0=",
                'LACAS Johar Town Girls':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvVhNJSsiAoDMzjGGfjLOn3MsJDskvQOP6pxTIJDqIJLd63kAZ5ymGwj9LGWCEFBq0=",
                'LACAS Johar Town Preschool':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvJDl6xpxwXWT81A3Tyw71lgL+HPkmtHQUGu1301pcjWkVG6StVJGlc1wf4zpzlmU8=",
                'Milestone Model Town Campus':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Euvf1i+xmUPIxmuBbZDHa8pxcqoYIXK90PyjqZpWjQCybk4jXjv5AfCHR0yL5eVRWk=",
                'Milestone Muslim Town Campus':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EthDWAcjUshNdWkMCGMXRrkO4E2xI/Su3Htuu2fqnWd1nmO82I0s7ZLX15o8XD7fGQ=",
                'Milestone Satellite Campus':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvGbYG0n5QbcqTCYDNGsb/56dFX+3fd+prljyAo/ZqSy75iTii/cy5UMuZbVef1Wis=",
                'Milestone Upper Mall Campus':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EsZwKzAHy9IvPdDUH58UdRf5EgcaMRRkHOf7TscdxY9IuHeuXoDAC3azV/P9TQT7lg=",
                'Milestone Valencia Campus':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EtlN0ghB6E5rDe1hC9kYe45vB6b26Zg+Ymzu7rr9W89Dg86wX4veamHfXvOG9M+gpU="
            }    
        for rec in std:
            
             
            fact_obj = Fact_Api()
            
            school_name = school_name_key[str(rec.school_ids.name)]
            fact_data = fact_obj.main(rec.facts_id,school_name)
            
            if 'student' in fact_data:
                student = fact_data['student']
                school = self.env['school.school'].search([('code','=',student['schoolCode'])])
                if school:
                    rec['school_ids'] = school
                #grade level
                for line in rec['enrollment_state_ids']:
                    if 'gradeLevel' in student['school']:
                        grade_obj = self.env['school.grade.level'].search([('name','=',student['school']['gradeLevel'])])
                        for i in grade_obj:
                            line['grade_level_id'] = i.id
                #next grade level                        
                if 'nextGradeLevel' in student['school']:
                    next_grade_obj = self.env['school.grade.level'].search([('name','=',student['school']['nextGradeLevel'])])
                    for i in next_grade_obj:
                        line['next_grade_level_id'] = i.id
                
                enrol_status_obj = self.env['school.enrollment.status'].search([])
                for i in enrol_status_obj: 
                    if 'nextStatus' in student['school'] and 'status' in student['school']:
                        if str(i.name) == str(student['school']['status']):
                            line['enrollment_status_id'] = i.id
                        if str(i.name) == str(student['school']['nextStatus']):
                            line['next_enrollment_status_id'] = i.id
            if 'pickup' in fact_data:
                pickup = fact_data['pickup']
            if 'people' in fact_data: 
                people = fact_data['people']
                first_name = people['firstName']
                middle_name = people['middleName']
                last_name = people['lastName']
                email = people['email']
                phone = people['homePhone']
                mobile = people['cellPhone']
                rec['first_name'] = first_name
                rec['last_name'] = last_name
                rec['middle_name'] = middle_name
                rec['email'] = email
                rec['phone'] = phone
                rec['mobile'] = mobile

            if 'personfamily' in fact_data:
                personfamily = fact_data['personfamily']
            if 'family' in fact_data:
                family = fact_data['family']
                
                rec.family_ids = False
                
                family_obj = self.env['school.family'].search([('facts_id','=',family['familyID'])])
                rec.family_ids = family_obj
                # if rec.family_ids:
                #     for fm_id in rec.family_ids: 
                #         if str(fm_id.name) == str(family['familyName']):
                #             family_obj = self.env['school.family'].search([('name','=',family['familyName'])])
                #             rec.family_ids = family_obj
                            
                #         else:
                #             rec.family_ids = False
                # else:
                #     family_obj = self.env['school.family'].search([('name','=',family['familyName'])])
                #     rec.family_ids = family_obj



            if 'demographic' in fact_data: 
                demographic = fact_data['demographic']
                gender = demographic['gender']
                birthdate = demographic['birthdate']
                rec['date_of_birth'] = birthdate
                gender_obj = self.env['school.gender'].search([('name','=',gender)])
                for i in gender_obj:
                    rec['gender'] = i.id 
            
            
                

      
                
                
                

            

            
            
            


            
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
            #     rec['olf_udid']=data['udid']
            #     rec['email'] = data['Email'] 
            #     rec['phone'] = data['Phone'] 
                  
                                                           
                                                    
                
                
