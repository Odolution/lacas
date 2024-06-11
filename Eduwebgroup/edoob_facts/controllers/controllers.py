# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolFacts(http.Controller):
#     @http.route('/school_facts/school_facts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_facts/school_facts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_facts.listing', {
#             'root': '/school_facts/school_facts',
#             'objects': http.request.env['school_facts.school_facts'].search([]),
#         })

#     @http.route('/school_facts/school_facts/objects/<model("school_facts.school_facts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_facts.object', {
#             'object': obj
#         })
