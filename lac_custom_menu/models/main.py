from odoo import models, api, fields, _
from odoo.exceptions import UserError

class field_changes_custom_update(models.Model):
    _inherit = 'account.move'
    udid_new_lv = fields.Char(compute='_compute_udid_student',string="UDID")
    facts_id_new_lv = fields.Char(compute='_compute_facts_id_student',string="Facts Id")

    
    def _compute_udid_student(self):
        # if self.move_type == "out_refund":
        for rec in self:
            if rec.student_ids:
                for stu_rec in rec.student_ids:
                    rec.udid_new_lv=stu_rec.facts_udid
            else:
                rec.udid_new_lv=""

            # for rec in self:
            # if rec.tuition_plan_ids:
            #     for stu_rec in rec.tuition_plan_ids:
            #         rec.udid_new_lv=stu_rec.student_id.facts_udid
            # else:
            #     rec.udid_new_lv=""

    def _compute_facts_id_student(self):
        # if self.move_type == "out_refund":
        for rec in self:
            if rec.student_ids:
                for stu_rec in rec.student_ids:
                    rec.facts_id_new_lv=stu_rec.facts_id
            else:
                rec.facts_id_new_lv=""
