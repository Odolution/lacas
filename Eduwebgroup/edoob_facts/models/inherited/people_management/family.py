# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SchoolBaseFamily(models.Model):
    """ Family model """

    ######################
    # Private Attributes #
    ######################
    _inherit = 'school.family'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################

    facts_id = fields.Integer("Facts ID")
    facts_udid = fields.Char("Facts UDID")
    family_name_bp = fields.Char("Family Name BP")

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
