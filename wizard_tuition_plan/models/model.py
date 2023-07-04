from odoo import models, api, fields


class wizard_tuition_plan(models.TransientModel):
    _name='tuition.wizard_tuition_plan'

    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    tuition_template_id = fields.Many2one('tuition.template', string='Tuition Template')

    
    # def apply(self):
    #     for lines in plan_ids:
    
    
    @api.onchange('template_id')
    def onchange_template_id(self):
        if self.template_id:
            raise UserError("same")
            self.plan_ids = self.template_id.plan_ids
        else:
            self.plan_ids = False

    
    
    
    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        ids=self._context.get("active_ids")
        res["plan_ids"]=[(6,0,ids)]
        return res
