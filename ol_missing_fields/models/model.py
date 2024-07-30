
from odoo import models, api, fields, _
from odoo.exceptions import UserError




class TutitionPlanInherit(models.Model):
    _inherit = "tuition.plan"
    enrollment_state = fields.Many2one('school.school', string="Enrollment State", compute='_compute_enrollment_state')
    
    def _compute_enrollment_state(self):
        for rec in self:
            if rec.student_id.enrollment_status_ids:
                first_status = rec.student_id.enrollment_status_ids[0]
                rec.enrollment_state = first_status 
            else:
                rec.enrollment_state = False
