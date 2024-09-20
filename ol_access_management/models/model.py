from odoo import models, fields

class AccessRights(models.Model):
    _name = 'access.rights'
    _description = 'Access Rights for Branch and Users'

    branch_id = fields.Many2one('school.program', string='Branch', required=True)
    user_ids = fields.Many2many('res.users', string='Users')
