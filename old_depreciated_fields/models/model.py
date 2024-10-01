# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SchoolFamily(models.Model):
    _inherit = 'school.family'

    olf_id = fields.Integer("olf ID")
    olf_udid = fields.Char("olf UDID")

class SchoolStudent(models.Model):
    _inherit = 'school.student'
    
    olf_udid = fields.Char(string="olf UDID")
    olf_id = fields.Integer(string="OLF ID", related='individual_id.olf_id', store=True)

class Partner(models.Model):
    _inherit = 'res.partner'

    olf_id = fields.Integer("olf ID")

class ProductCategory(models.Model):
    _inherit = 'product.category'

    olf_id = fields.Integer(string="olf id")


#studio fields

class AccountStudioField(models.Model):
    _inherit = 'account.move'

    x_studio_reg_id = fields.Char(string="OLF Id",related='x_student_id_cred.olf_udid')
    x_studio_related_field_KeYGh = fields.Char(string="New Related Field",related='x_student_id_cred.olf_udid')
    x_studio_student_code = fields.Integer(string="Student Code",related='x_student_id_cred.olf_id')