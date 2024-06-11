# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Program(models.Model):
    """ Program """
    ######################
    # Private Attributes #
    ######################
    _inherit = 'school.program'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    school_code_name = fields.Char('School Code Name', related='school_id.code')
    is_facts_program = fields.Boolean('Is Facts Program?')
    ##################
    # Compute method #
    ##################

    #########################
    # CRUD method overrides #
    #########################
