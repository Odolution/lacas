# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions


class SchoolClass(models.Model):
    ######################
    # Private Attributes #
    ######################
    _inherit = 'school.class'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    facts_id = fields.Integer("Facts ID")

    ##############################
    # Compute and search methods #
    ##############################

    ###########################
    # Constrains and onchange #
    ###########################

    #########################
    # CRUD method overrides #
    #########################
