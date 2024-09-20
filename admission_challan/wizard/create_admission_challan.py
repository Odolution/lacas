from odoo import api, fields, models

class AdmissionChallanWizard(models.TransientModel):
    _name = "admission.challan.wizard"
    _description = "Admission Challan Wizard"

    template_id = fields.Many2one('tuition.template', string="Fee Template", required=True)
    
    def action_create_tuition_plan(self):
        self.ensure_one()
        if self.template_id:
            # Call the function on the template_id (tuition.template)
            self.template_id.button_new_tuition_plan()
        return {'type': 'ir.actions.act_window_close'}

    def action_discard(self):
        return {'type': 'ir.actions.act_window_close'}
