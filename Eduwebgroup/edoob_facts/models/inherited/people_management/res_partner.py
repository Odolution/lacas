# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SchoolStudent(models.Model):
    _inherit = 'school.student'
    
    facts_udid = fields.Char(string="Facts UDID")


class SchoolBaseFamily(models.Model):
    """ Family model """

    ######################
    # Private Attributes #
    ######################
    _inherit = 'res.partner'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################

    facts_id = fields.Integer("Facts ID")
    facts_nickname = fields.Char("Facts nickname")
    salutation = fields.Char("Salutation")
    suffix = fields.Char("Suffix")

    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
