# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, SUPERUSER_ID


class TuitionTemplateInstallment(models.Model):
    _name = "tuition.template.installment"
    _inherit = 'tuition.installment.mixin'
    _description = "Tuition Plan Installment"

    tuition_template_id = fields.Many2one("tuition.template", "Tuition template", required=True, ondelete="cascade")

    lines_ids = fields.Many2many(
        'tuition.template.line',
        relation='tuition_template_installment_template_line_rel',
        column1='installment_id',
        column2='line_id',
        string="Lines")

    def get_installment_values(self):
        values = [
            {
                'name': installment.name,
                'sequence': installment.sequence,
                'type': installment.type,
                'day_type': installment.day_type,
                'day_of_the_month': installment.day_of_the_month,
                'month': installment.month,
                'date': installment.date,
                'template_installment_id': installment.id,
                'quarter': installment.quarter,
                } for installment in self]
        return values

    def _get_monthly_date(self):
        self.ensure_one()
        if not self.month:
            return False
        today = fields.Date.today()
        if self.day_type == 'last_day':
            day = 31
        elif self.day_type == 'day_number':
            day = int(self.day_of_the_month)
        else:
            day = 1
        next_date = today + relativedelta(month=int(self.month), day=day)
        next_date = self.move_next_year_if_needed(next_date)
        return next_date

    def get_previous_installment(self):
        sorted_sibling_installments = self.tuition_template_id.installment_ids.sorted('sequence')
        previous_installment = self.browse()
        for i, installment in enumerate(sorted_sibling_installments):
            if i == 0 and installment == self:
                break
            elif installment == self:
                previous_installment = sorted_sibling_installments[i - 1]
        return previous_installment

    def get_next_installment(self):
        sorted_sibling_installments = self.tuition_template_id.installment_ids.sorted('sequence', reverse=True)
        next_installment = self.browse()
        for i, installment in enumerate(sorted_sibling_installments):
            if i == 0 and installment == self:
                break
            elif installment == self:
                next_installment = sorted_sibling_installments[i - 1]
        return next_installment

    def get_parent(self):
        self.ensure_one()
        return self.tuition_template_id
