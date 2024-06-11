# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class CreateBulkTuitionPLan(models.TransientModel):
    _name = 'create.bulk.tuition.plan'
    _description = "Create bulk tuition plan"

    student_ids = fields.Many2many('school.student', required=True, string="Students")
    tuition_template_id = fields.Many2one('tuition.template', required=True, string="Tuition template")

    post_tuition_plans = fields.Boolean(string="Post tuition plans")

    def button_generate_tuition_plans(self):
        self.ensure_one()
        tuition_plans = self._generate_tuition_plans()
        if self.post_tuition_plans:
            tuition_plans.post()
        return self.action_view_tuition_plans(tuition_plans)

    def _generate_tuition_plans(self):
        tuition_plans = self.env['tuition.plan']
        for student in self.student_ids:
            tuition_plan = self.env['tuition.plan'].with_context(self._context).create({
                'student_id': student.id,
                'pricelist_id': student.property_product_pricelist and student.property_product_pricelist.id or False,
                'payment_term_id': student.property_payment_term_id and student.property_payment_term_id.id or False,
                })
            tuition_plans += tuition_plan
        return tuition_plans

    def action_view_tuition_plans(self, tuition_plans):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('edoob_finance.tuition_plan_action')
        if len(tuition_plans) > 1:
            action['domain'] = [('id', 'in', tuition_plans.ids)]
        elif len(tuition_plans) == 1:
            form_view = [(self.env.ref('edoob_finance.tuition_plan_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = tuition_plans.id
        else:
            action = {
                'type': 'ir.actions.act_window_close'
                }

        if len(self) == 1:
            context = {
                'default_tuition_template_id': self.tuition_template_id.id,
                }
            action['context'] = context
        return action
