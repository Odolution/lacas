from odoo import models, api, fields
from odoo.exceptions import UserError
import json
import datetime


class wizard_tuition_plan(models.TransientModel):
    _name='tuition.wizard_tuition_plan'

    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    tuition_template_id = fields.Many2one('tuition.template', string='Tuition Template')

    
    def apply(self):
        
        tuition_lines=self.tuition_template_id.line_ids

        for t_plan in self.plan_ids:
            for lines in t_plan.line_ids:
                for line in tuition_lines:
                    if lines.product_id==line.product_id:
                        if lines.unit_price!=line.unit_price:
                            lines.unit_price=line.unit_price
                    else:
                        t_plan= self.env['tution.plan'].browse(line_ids)
                        new_line = self.env['tuition.plan.line'].new({
                                'product_id': line.product_id,
                                'plan_id': t_plan.id,
                                'currency_id':1,
                                'name':line.name,
                                # Add other field values as needed
                            })
                        t_plan.line_ids += new_line
                 

         

    
    
    
    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        ids=self._context.get("active_ids")
        res["plan_ids"]=[(6,0,ids)]
        return res
