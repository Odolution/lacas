# -*- coding: utf-8 -*-
from lxml import etree

from odoo import models, fields, api, _
from odoo.fields import Command
import logging

logger = logging.getLogger(__name__)


def isInt(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


class EnrollStudentForm(models.TransientModel):
    """ Enrollment Students Form """
    _inherit = 'enroll.student.form'

    state = fields.Selection(selection_add=[("30", "Tuition plan")], ondelete={'30': 'cascade'})

    tuition_template_id = fields.Many2one('tuition.template')
    post_tuition_plans = fields.Boolean(string="Confirm tuition plans after creation", default=True)

    def on_move_step_30(self, prev_state, new_state):
        # self.recompute_relationships()
        pass

    def _student_created(self):
        super()._student_created()
        for student in self.student_ids:
            self._create_tuition_plan_for_student(student)

    def _create_tuition_plan_for_student(self, student):
        BulkTuitionPlan = self.env['create.bulk.tuition.plan'].sudo()
        context = {**self._context, 'take_tuition_template_values': True, 'default_tuition_template_id':  self.tuition_template_id.id}
        bulk_creation = BulkTuitionPlan.with_context(context).create({
            'student_ids': [Command.set(student.real_student_id.ids)],
            'tuition_template_id': self.tuition_template_id.id,
            'post_tuition_plans': self.post_tuition_plans
            })
        action = bulk_creation.button_generate_tuition_plans()
        return action