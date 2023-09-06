import logging
from odoo import api, fields, models
from odoo.exceptions import UserError
import requests
import ast

class SchoolStudent(models.Model):
    _inherit = "school.student"

    def get_homeroom(self):
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
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': ''
        } 
        # api_key = 'ejlLPL5VblvTyZXkE5fgvfuOyMnjWYJhVYe69A6l/EuIhXl6zCq8G/1abw2CTbjMnyQCEygm1dQE+p1fYauQRJ2/34/RKM5maKAUi6lhn3A='
        students = self.env['school.student'].search([('homeroom', '=', False)])
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
