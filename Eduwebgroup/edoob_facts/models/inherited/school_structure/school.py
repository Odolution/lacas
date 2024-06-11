# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions


class SchoolSchool(models.Model):
    ######################
    # Private Attributes #
    ######################
    _inherit = 'school.school'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    facts_school_id = fields.Char("Facts School ID")
    ##############################
    # Compute and search methods #
    ##############################

    ###########################
    # Constrains and onchange #
    ###########################

    #########################
    # CRUD method overrides #
    #########################
