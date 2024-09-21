from odoo import api, fields, models
from odoo.exceptions import UserError

class AdmissionChallanWizard(models.TransientModel):
    _name = "admission.challan.wizard"
    _description = "Admission Challan Wizard"

    template_id = fields.Many2one('tuition.template', string="Fee Template", required=True)
    student_id = fields.Many2one('school.student', string="Student")
    # student_ids = fields.Many2one('school.student', string="Student")
    
    def action_create_tuition_plan(self):
        self.ensure_one()
        if self.template_id:

            student_ids = self.env.context.get('student_ids')
            if student_ids:
                for sid in student_ids:                    
                    context = {**self._context, 'take_tuition_template_values': True, 'default_tuition_template_id':  self.tuition_template_id.id}
                    self.env['tuition.plan'].with_context(context).create({
                    'student_id': sid,
                    'tuition_template_id': self.template_id.id,
                })
            else:
                # Call the function on the template_id (tuition.template)
                self.env['tuition.plan'].create({
                'student_id': self.student_id.id,
                'tuition_template_id': self.template_id.id,
            })
        return {'type': 'ir.actions.act_window_close'}

    def action_discard(self):
        return {'type': 'ir.actions.act_window_close'}
