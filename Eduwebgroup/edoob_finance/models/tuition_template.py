# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.fields import Command
from babel.dates import format_date
import json
from datetime import datetime, timedelta
from odoo.tools.misc import get_lang
import random


class TuitionTemplate(models.Model):
    _name = 'tuition.template'
    _description = 'Tuition template'
    _inherit = 'tuition.plan.mixin'

    active = fields.Boolean(default=True)
    line_ids = fields.One2many('tuition.template.line', 'template_id')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')
    installment_ids = fields.One2many('tuition.template.installment', 'tuition_template_id', string="Installments")
    tuition_plan_ids = fields.One2many('tuition.plan', 'tuition_template_id', string="Tuition plans")
    tuition_plan_count = fields.Integer(string="Tuition plan count", compute='compute_tuition_plan_count')

    installment_template = fields.Selection(selection=[
        ('quarterly', "Quarterly"),
        ('biannually', "Bi-Annually"),
        ('monthly', "Monthly"),
        ('yearly', "Yearly"),
        ], default='quarterly', string="Installment template")

    @api.onchange('program_id')
    def onchange_program_id(self):
        self.line_ids.grade_level_ids = False

    @api.onchange('installment_template')
    def onchange_installment_template(self):
        self.ensure_one()
        self.line_ids.installment_ids = False
        if self.installment_template == 'quarterly':
            self.set_quarterly_installment()
        elif self.installment_template == 'monthly':
            self.set_monthly_installment()
        elif self.installment_template == 'biannually':
            self.set_biannually_installment()
        elif self.installment_template == 'yearly':
            self.set_yearly_installment()

    @api.depends('tuition_plan_ids')
    def compute_tuition_plan_count(self):
        for template in self:
            template.tuition_plan_count = len(template.tuition_plan_ids)

    def button_new_tuition_plan(self):
        context = {'take_tuition_template_values': True, 'default_tuition_template_id': self.id}
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'create.bulk.tuition.plan',
            'view_mode': 'form',
            'target': 'new',
            'context': context
            }

    def _kanban_dashboard_graph(self):
        for template in self:
            template.kanban_dashboard_graph = json.dumps(template.get_bar_graph_datas())

    def get_bar_graph_datas(self):
        self.ensure_one()
        today = fields.Datetime.now(self)

        all_months = [datetime(today.year, month, 1) for month in range(1, 13)]
        labels = [format_date(month, 'MMMM', locale=get_lang(self.env).code) for month in all_months]
        return [{
            'labels': labels,
            'values': [{
                'label': "Income",
                'values': [random.randint(i, i*10) for i in range(0, 12)],
                'type': 'income',
                }, {
                'label': "Due",
                'values': [random.randint(i, i*10) for i in range(0, 12)],
                'type': 'due',
                }]
            }]

    def action_view_tuition_plans(self):
        self.ensure_one()
        tuition_plans = self.tuition_plan_ids
        action = self.env['ir.actions.actions']._for_xml_id('edoob_finance.tuition_plan_action')
        if len(tuition_plans) > 1:
            action['domain'] = [('id', 'in', tuition_plans.ids)]
        elif len(tuition_plans) == 1:
            form_view = [(self.env.ref('edoob_finance.tuition_plan_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = tuition_plans.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        if len(self) == 1:
            context = {
                'default_tuition_template_id': self.id,
                }
            action['context'] = context
        return action

    def set_quarterly_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q1',
                    'month': '9',
                    'day_type': 'first_day',
                    'sequence': 1
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q2',
                    'month': '12',
                    'day_type': 'first_day',
                    'sequence': 2
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q3',
                    'month': '3',
                    'day_type': 'first_day',
                    'sequence': 3
                    }),
                Command.create({
                    'type': 'quarterly',
                    'quarter': 'Q4',
                    'month': '6',
                    'day_type': 'first_day',
                    'sequence': 4
                    }),
                ]

    def set_monthly_installment(self):
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'monthly',
                    'month': '1',
                    'day_type': 'first_day',
                    'sequence': 1,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '2',
                    'day_type': 'first_day',
                    'sequence': 2,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '3',
                    'day_type': 'first_day',
                    'sequence': 3,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '4',
                    'day_type': 'first_day',
                    'sequence': 4,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '5',
                    'day_type': 'first_day',
                    'sequence': 5,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '6',
                    'day_type': 'first_day',
                    'sequence': 6,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '7',
                    'day_type': 'first_day',
                    'sequence': 7,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '8',
                    'day_type': 'first_day',
                    'sequence': 8,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '9',
                    'day_type': 'first_day',
                    'sequence': 9,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '10',
                    'day_type': 'first_day',
                    'sequence': 10,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '11',
                    'day_type': 'first_day',
                    'sequence': 11,
                    }),
                Command.create({
                    'type': 'monthly',
                    'month': '12',
                    'day_type': 'first_day',
                    'sequence': 12,
                    }),
                ]

    def set_biannually_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'biannually',
                    'month': '9',
                    'sequence': 1,
                    }),
                Command.create({
                    'type': 'biannually',
                    'month': '1',
                    'sequence': 2,
                    }),
                ]

    def set_yearly_installment(self):
        self.ensure_one()
        self.installment_ids = [
                Command.clear(),
                Command.create({
                    'type': 'yearly',
                    'month': '1',
                    'day_type': 'first_day',
                    'sequence': 1,
                    }),
                ]

