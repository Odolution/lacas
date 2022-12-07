from odoo import models, api, fields, _
from odoo.exceptions import UserError

class field_changes_custom_update(models.Model):
    _inherit = 'account.move'
    udid_new_lv = fields.Char(compute='_compute_udid_student',string="UDID NEW")

    
    def _compute_udid_student(self):
        # if self.move_type == "out_refund":
        for rec in self:
            if rec.tuition_plan_ids:
                for stu_rec in rec.tuition_plan_ids:
                    rec.udid_new_lv=stu_rec.student_id.facts_udid
            else:
                rec.udid_new_lv=""
