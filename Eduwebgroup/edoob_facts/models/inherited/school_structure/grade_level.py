# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SchoolBaseGradeLevel(models.Model):
    """ Grade levels """

    ######################
    # Private Attributes #
    ######################
    _inherit = 'school.grade.level'

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
