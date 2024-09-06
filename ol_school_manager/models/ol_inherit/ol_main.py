# -*- coding: utf-8 -*-

# ir.http

from odoo import models, fields, api, _, tools
from odoo.addons.website.models import ir_http
from odoo.exceptions import ValidationError
from odoo.fields import Command

import logging

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        session_info = super(IrHttp, self).session_info()
        user = self.env.user

        if user.has_group('base.group_user'):
            programs = self.env.user.user_program_ids
            schools = programs.mapped('school_id')
            districts = schools.mapped('district_id')

            district_vals_list = districts.read(['name'])
            current_district_vals = district_vals_list[0] if district_vals_list else {}

            school_vals_list = []
            for i, school_vals, in enumerate(schools.read(['name'])):
                school_vals['district_id'] = schools[i].district_id.id
                school_vals_list.append(school_vals)

            current_school_vals = school_vals_list[0] if school_vals_list else {}

            program_vals_list = []
            for i, program_vals, in enumerate(programs.read(['name'])):
                program_vals['school_id'] = programs[i].school_id.id
                program_vals['parent_id'] = programs[i].parent_id.id
                program_vals['child_ids'] = programs[i].child_ids.ids
                program_vals_list.append(program_vals)
            current_program_vals = program_vals_list[0] if program_vals_list else {}

            session_info.update({
                'user_districts': {
                    'current_district': current_district_vals,
                    'allowed_districts': district_vals_list,
                },
                'user_schools': {
                    'current_school': current_school_vals,
                    'allowed_schools': school_vals_list,
                },
                'user_programs': {
                    'current_program': current_program_vals,
                    'allowed_programs': program_vals_list,
                },
                'display_switch_school_menu': bool(self.env.user.user_program_ids)
            })

        return session_info

class IrRule(models.Model):
    _inherit = 'ir.rule'

    @api.model
    def _eval_context(self):
        res = super(IrRule, self)._eval_context()
        res.update({
            'district_id': self.env.district.id,
            'district_ids': self.env.districts.ids,

            'school_id': self.env.school.id,
            'school_ids': self.env.schools.ids,

            'program_id': self.env.program.id,
            'program_ids': self.env.programs.ids,
            })
        return res

    def _compute_domain_keys(self):
        """ Return the list of context keys to use for caching
         ``_compute_domain``. """
        return super(IrRule, self)._compute_domain_keys() \
               + ['allowed_program_ids']

class Company(models.Model):
    _inherit = "res.company"

    district_id = fields.Many2one("school.district", "District")
    district_ids = fields.Many2many(
        "school.district", string="Districts",
        relation='district_company_rel', column1='company_id', column2='district_id')

    district_school_ids = fields.One2many(
        "school.school", string="District schools",
        related="district_ids.school_ids")

    school_id = fields.Many2one('school.school', string="School")
    school_ids = fields.Many2many(
        'school.school', string="Schools",
        relation='school_company_rel', column1='company_id', column2='school_id')
    district_name = fields.Char(related="district_id.name", string="District name")

    current_school_year_id = fields.Many2one('school.period', string="Current school year")
    enrollment_school_year_id = fields.Many2one('school.period', string="Enrollment school year")

    @api.onchange('district_ids')
    def _onchange_school_ids(self):
        for company in self:
            company.school_ids = company.district_ids.mapped('school_ids')

class Contact(models.Model):
    """ Contact """

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
    is_ol_student = fields.Boolean("School student", compute='_compute_is_ol_partner', store=True)
    is_ol_partner = fields.Boolean("School partner", compute='_compute_is_ol_partner', store=True)
    is_ol_parent = fields.Boolean("School parent", compute='_compute_is_ol_partner', store=True)
    is_ol_individual = fields.Boolean("School individual", compute='_compute_is_ol_partner', store=True)
    school_individual_ids = fields.One2many('school.family.individual', 'partner_id', string="Related individuals")
    student_ids = fields.One2many('school.student', 'partner_id', string="Related student")

    # Search fields

    # Address fields
    address_partner_link_id = fields.Many2one('res.partner', string="Address partner link")
    partner_with_address_link_as_me_ids = fields.One2many(
        'res.partner', 'address_partner_link_id', 
        string="Partner with address link as me")

    @api.constrains('address_partner_link_id')
    def _check_address_partner_link_id(self):
        for partner in self:
            if not partner._check_recursion('address_partner_link_id'):
                raise ValidationError(_("You cannot create recursive partner addresses"))

    ##############################
    # Compute and search methods #
    ##############################
    @api.depends('school_individual_ids', 'student_ids')
    def _compute_is_ol_partner(self):
        for partner in self:
            is_ol_individual = bool(partner.school_individual_ids)
            is_ol_student = bool(partner.student_ids)
            is_school_parent = is_ol_individual and not is_ol_student

            partner.is_ol_partner = is_ol_individual
            partner.is_ol_individual = is_ol_individual
            partner.is_ol_parent = is_school_parent
            partner.is_ol_student = is_ol_student

    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################
    def write(self, values):
        res = super().write(values)
        if 'address_partner_link_id' in values:
            for partner in self:
                if partner.address_partner_link_id:
                    partner.write(partner.address_partner_link_id._prepare_write_recursive_address_links_values())
        if 'address_partner_link_id' not in values:
            if set(values.keys()) & self._get_address_link_fields():
                self._update_recursive_address_links()
        return res

    @api.model
    def create(self, values):
        partner = super().create(values)
        #
        # if set(values.keys()) & self._get_address_link_fields():
        #     # if not self._context.get('skip_recursive_check', False):
        #     partner._update_recursive_address_links()
        return partner

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################
    @api.model
    def _get_address_link_fields(self):
        return {'country_id', 'state_id', 'city', 'street', 'street2', 'zip'}

    def _update_recursive_address_links(self):
        for partner in self:
            partners_to_update = partner.address_partner_link_id + partner.partner_with_address_link_as_me_ids
            partners_to_update = partners_to_update.filtered(partner._check_partner_has_not_same_address_fields)
            partners_to_update.write(partner._prepare_write_recursive_address_links_values())
            # partners_to_update._update_recursive_address_links()

    def _check_partner_has_not_same_address_fields(self, partner):
        self.ensure_one()
        for field in self._get_address_link_fields():
            if self[field] != partner[field]:
                return True
        return False

    def _prepare_write_recursive_address_links_values(self):
        self.ensure_one()
        address_values = {}
        for field in self._get_address_link_fields():
            field_type = self.env['res.partner']._fields[field]
            if field_type.type == 'many2one':
                if self[field]:
                    address_values[field] = self[field].id
            else:
                address_values[field] = self[field]
        return address_values


class ResUsers(models.Model):
    _inherit = 'res.users'

    user_school_id = fields.Many2one(
        'school.school', string="User school", compute_sudo='_compute_school_fields', store=True)
    user_school_ids = fields.Many2many(
        'school.school', 'res_school_users_rel', 'user_id', 'school_id', string="User schools",
        compute_sudo='_compute_school_fields', store=True)
    user_district_id = fields.Many2one('school.district', compute_sudo='_compute_school_fields', store=True)
    user_district_ids = fields.Many2many(
        'school.district', 'res_district_users_rel', 'user_id', 'district_id',
        compute_sudo='_compute_school_fields', store=True)

    user_program_id = fields.Many2one(
        'school.program', string='School program',
        help='The default program for this user.')
    user_program_ids = fields.Many2many(
        'school.program', 'res_program_users_rel', 'user_id', 'pid',
        string='School programs', default=lambda self: self.env.programs.ids)

    @api.constrains('user_program_id', 'user_program_ids')
    def _check_program(self):
        for user in self:
            if user.user_program_ids and not user.user_program_id:
                raise ValidationError(_('School program cannot be empty if you are assigning programs to an user (%s)', user.name))
            if user.user_program_ids and user.user_program_id not in user.user_program_ids:
                raise ValidationError(
                    _('School program %(proram_name)s is not in the allowed school programs for user %(user_name)s (%(program_allowed)s).',
                      proram_name=user.user_program_id.name,
                      user_name=user.name,
                      program_allowed=', '.join(user.mapped('user_program_ids.name')))
                )

    @api.onchange('user_program_ids')
    def onchange_program_ids(self):
        if self.user_program_id not in self.user_program_ids:
            self.user_program_id = self.user_program_ids[:1]._origin

    @api.depends('user_program_id', 'user_program_ids')
    def _compute_school_fields(self):
        for user in self:
            user.user_school_id = user.user_program_id.school_id
            user.user_school_ids = user.user_program_ids.mapped('school_id')
            user.user_district_id = user.user_program_id.school_id.district_id
            user.user_district_ids = user.user_program_ids.mapped('school_id.district_id')

    @api.model_create_multi
    def create(self, vals_list):
        new_vals_list = []
        for values in vals_list:
            new_vals_list.append(self._remove_reified_groups(values))
        users = super().create(new_vals_list)
        group_multi_company_id = self.env['ir.model.data']._xmlid_to_res_id('school.group_multi_company', raise_if_not_found=False)
        if group_multi_company_id:
            for user in users:
                if len(user.company_ids) <= 1 and group_multi_company_id in user.groups_id.ids:
                    user.write({'groups_id': [Command.unlink(group_multi_company_id)]})
                elif len(user.company_ids) > 1 and group_multi_company_id not in user.groups_id.ids:
                    user.write({'groups_id': [Command.link(group_multi_company_id)]})
        return users

    def write(self, values):
        values = self._remove_reified_groups(values)
        res = super().write(values)
        if 'company_ids' not in values:
            return res
        group_multi_company = self.env.ref('base.group_multi_company', False)
        if group_multi_company:
            for user in self:
                if len(user.company_ids) <= 1 and user.id in group_multi_company.users.ids:
                    user.write({'groups_id': [Command.unlink(group_multi_company.id)]})
                elif len(user.company_ids) > 1 and user.id not in group_multi_company.users.ids:
                    user.write({'groups_id': [Command.link(group_multi_company.id)]})
        return res

