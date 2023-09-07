import logging
from odoo import api, fields, models
from odoo.exceptions import UserError
import requests
import ast

class SchoolStudent(models.Model):
    _inherit = "school.student"

    # def get_user_defined_fields_data(self, students):
    #     headers = {
    #         'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
    #         'Facts-Api-Key': ''
    #     } 


    #     grade_level_id = 320
    #     mother_cnic_id = 219
    #     father_cnic_id = 220

    #     # students = self.env['school.student'].search([('homeroom', '=', False), ('x_last_enrollment_status_id.name', '=', 'Enrolled')])
    #     for std in students:
    #         api_key = school_name_key.get(std.x_last_school_id.name)
    #         headers['Facts-Api-Key'] = api_key

    #         # Father CNIC
    #         url = f"https://api.factsmgt.com/UserDefinedData?Page=1&api-version=1&filters=linkedId=={std.facts_id},fieldId=={father_cnic_id}"
    #         response = requests.request("GET", url, headers=headers).json()
    #         if response.get('results') and len(response.get('results')) > 0:
    #             std.x_studio_father_cnic = response.get('results')[0]['data']
            
    #         # Mother CNIC
    #         url = f"https://api.factsmgt.com/UserDefinedData?Page=1&api-version=1&filters=linkedId=={std.facts_id},fieldId=={mother_cnic_id}"
    #         response = requests.request("GET", url, headers=headers).json()
    #         if response.get('results') and len(response.get('results')) > 0:
    #             std.x_studio_mother_cnic = response.get('results')[0]['data']

    #         # Grade Level
    #         url = f"https://api.factsmgt.com/UserDefinedData?Page=1&api-version=1&filters=linkedId=={std.facts_id},fieldId=={grade_level_id}"
    #         response = requests.request("GET", url, headers=headers).json()
    #         if response.get('results') and len(response.get('results')) > 0:
    #             std.x_studio_grade_level = response.get('results')[0]['data']

        
    def get_homeroom_and_custom_defined_fields(self, timeline='daily'):
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
                'Milestone Valencia Campus':"ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EtlN0ghB6E5rDe1hC9kYe45vB6b26Zg+Ymzu7rr9W89Dg86wX4veamHfXvOG9M+gpU=",
                'Milestone Model Town Campus': "ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvTFCkn5V/wFqP+d3CHeBNzLfXX/ZwjCbtWmp/Zv3Ih8/SsLvD6KX8GLqZHbk/ZsM0=",
                'Milestone Model Town Senior Campus': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EsGJHcioGvg6uL1doVglkRyhKwkbCFXTaymG9pmLwZwlAGe4U8dQWGXqBref8Xb4VE=',
                'Milestone Muslim Town (Matric)': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/Evd1rLR/9C+I1nmDiAv2rpwRKorQgVh3dvn7XqZbqsTj5klXsVOR1X+jCExuTFcvww=',
                'Milestone Upper Mall (Matric)': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuEvn4hhx929JAhljKEBitMMvJbEW/ebJjmxtu7kD/M0ikd2oW0teUkCOG4Hx99H98=',
                'Milestone Valencia (Matric)': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EsOBT+5pIck8rUW8gynOeRZZBETlgQhT74zLObeKMiIDI1+ya4G2Cj9WT4/EP7ZrZI=',
                'Milestone Model Town (Matric)': 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EvTFCkn5V/wFqP+d3CHeBNzLfXX/ZwjCbtWmp/Zv3Ih8/SsLvD6KX8GLqZHbk/ZsM0=',

            }
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': ''
        } 
        # api_key = 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuIhXl6zCq8G/1abw2CTbjMnyQCEygm1dQE+p1fYauQRJ2/34/RKM5maKAUi6lhn3A='
        if timeline == 'daily':
            students = self.env['school.student'].search([('homeroom', '=', False), ('x_last_enrollment_status_id.name', '=', 'Enrolled')])
        else:
            students = self.env['school.student'].search([('x_last_enrollment_status_id.name', '=', 'Enrolled')])
        
        for std in students:
            api_key = school_name_key.get(std.x_last_school_id.name)
            headers['Facts-Api-Key'] = api_key
            
            if len(std.grade_level_ids) >= 1:
                grade_level = std.grade_level_ids[0].name
                if grade_level:
                    url = f"https://api.factsmgt.com/academics/Enrollments?filters=studentId=={std.facts_id}"
                    response = requests.request("GET", url, headers=headers).json()
                    for record in response['results']:
                        class_id = record.get('classId')
                        url = f"https://api.factsmgt.com/Classes/v2?filters=classId=={class_id}"
                        response = requests.request("GET", url, headers=headers).json()['results']
                        if len(response) > 0:
                            section = response[0].get('section')
                            if section:
                                homeroom = grade_level + '-' + section
                                std.homeroom = homeroom
                                break
            grade_level_id = 320
            mother_cnic_id = 219
            father_cnic_id = 220
            
            # Father CNIC
            url = f"https://api.factsmgt.com/UserDefinedData?Page=1&api-version=1&filters=linkedId=={std.facts_id},fieldId=={father_cnic_id}"
            response = requests.request("GET", url, headers=headers).json()
            if response.get('results') and len(response.get('results')) > 0:
                std.x_studio_father_cnic = response.get('results')[0]['data']
            
            # Mother CNIC
            url = f"https://api.factsmgt.com/UserDefinedData?Page=1&api-version=1&filters=linkedId=={std.facts_id},fieldId=={mother_cnic_id}"
            response = requests.request("GET", url, headers=headers).json()
            if response.get('results') and len(response.get('results')) > 0:
                std.x_studio_mother_cnic = response.get('results')[0]['data']

            # Grade Level
            url = f"https://api.factsmgt.com/UserDefinedData?Page=1&api-version=1&filters=linkedId=={std.facts_id},fieldId=={grade_level_id}"
            response = requests.request("GET", url, headers=headers).json()
            if response.get('results') and len(response.get('results')) > 0:
                std.x_studio_grade_level = response.get('results')[0]['data']
