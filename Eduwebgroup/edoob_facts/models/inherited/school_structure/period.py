# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Period(models.Model):
    """ Period """

    ######################
    # Private Attributes #
    ######################
    _inherit = 'school.period'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    facts_id = fields.Integer("Facts ID")
    facts_year_id = fields.Integer("Facts Yead ID")
    facts_semester_id = fields.Integer("Facts Semester ID")
    facts_unique_term_id = fields.Integer("Facts Unique Term ID")
    parent_code = fields.Char("Parent Code", compute='_get_parent_code', store=True)
    
    category_facts_type = fields.Selection(related='category_id.facts_type', store=True)
    
    ##################
    # Compute method #
    ##################
    @api.depends('parent_id.code')
    def _get_parent_code(self):
        for period in self:
            period.parent_code = period.parent_id.code

class PeriodCategory(models.Model):
    """ Period """

    ######################
    # Private Attributes #
    ######################
    _inherit = 'school.period.category'

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    facts_type = fields.Selection(
        selection=[
            ('facts_year', "Year"),
            ('facts_semester', "Semester"),
            ('facts_term', "Term"),
        ], string="Facts type", default=False)