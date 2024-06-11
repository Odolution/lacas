# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from odoo.addons.account.models.company import MONTH_SELECTION
from dateutil.relativedelta import relativedelta
from odoo.tools import format_datetime
from datetime import datetime
from odoo.tools import html2plaintext, is_html_empty, plaintext2html, DEFAULT_SERVER_DATETIME_FORMAT as dtf
from odoo.tools.misc import get_lang


class TuitionPlanInstallment(models.AbstractModel):
    _name = "tuition.installment.mixin"
    _description = "Tuition Plan Installment mixin"
    _order = "sequence,id"
    _rec_name = "name"

    name = fields.Char(store=False, compute='_compute_name')
    sequence = fields.Integer(default=10, index=True)
    real_date = fields.Date(
        store=False, string="Real date", required=True, compute='_compute_real_date')
    date = fields.Date(string="Date", help="Date to trigger installment", required=True, default=lambda self: fields.Date.today())
    type = fields.Selection(selection=[
        ('monthly', "Monthly"),
        ('quarterly', "Quarterly"),
        ('biannually', "Bi-annually"),
        ('yearly', "Yearly"),
        ('exact_date', "Exact date"),
        ], string="Type", default='monthly', required=True)
    day_type = fields.Selection(selection=[
        ('first_day', "First day"),
        ('last_day', "Last day"),
        ('day_number', "Day number"),
        ], string="Day type", default='first_day')
    day_of_the_month = fields.Integer(string="Day of the month")
    month = fields.Selection(selection=MONTH_SELECTION, string="Month", default='1')

    quarter = fields.Selection(selection=[
        ('Q1', "Q1"),
        ('Q2', "Q2"),
        ('Q3', "Q3"),
        ('Q4', "Q4"),
        ], string="Quarter", default='Q1')

    @api.depends('date', 'type', 'month')
    def _compute_name(self):
        month_selection = dict(self._fields['month'].selection)
        quarter_selection = dict(self._fields['quarter'].selection)
        for installment in self:
            if installment.type == 'monthly':
                installment.name = month_selection.get(installment.month)
            elif installment.type == 'quarterly':
                installment.name = quarter_selection.get(installment.quarter)
            elif installment.type == 'biannually':
                installment.name = _("Bi-annually")
            elif installment.type == 'yearly':
                installment.name = _("Yearly")
            elif installment.type == 'exact_date':
                installment.name = installment.date
            else:
                installment.name = _("Installment")

    def _compute_real_date(self):
        for installment in self:
            if installment.type == 'exact_date':
                installment.real_date = installment.date
            elif installment.type in ('monthly', 'quarterly', 'biannually', 'yearly') and installment.month:
                installment.real_date = installment._get_monthly_date()
            else:
                installment.real_date = False

    def _get_monthly_date(self):
        return False

    def move_next_year_if_needed(self, next_date):
        previous_installment = self.get_previous_installment()
        if previous_installment and previous_installment.real_date:
            while next_date < previous_installment.real_date:
                next_date = next_date + relativedelta(years=1)
            # Fix February, 29th
            if next_date.month == 2 and (self.day_type == 'last_day' or (self.day_type == 'day_number' and self.day_of_the_month > 28)):
                next_date = next_date + relativedelta(day=31)
        return next_date

    def get_previous_installment(self):
        return False

    def get_next_installment(self):
        return False

    def get_parent(self):
        self.ensure_one()
        return False

    @api.constrains('month', 'day_of_the_month')
    def constraint_day_of_the_month_depends_on_month(self):
        for installment in self:
            day_of_the_month = installment.day_of_the_month
            month = int(installment.day_of_the_month)
            if day_of_the_month:
                if day_of_the_month < 1:
                    raise ValidationError(_('Having negative "day of the month" does not make sense'))
                if day_of_the_month > 31:
                    raise ValidationError(_("There is no month with more than 31 days"))
                if month in (4, 6, 9, 11) and day_of_the_month > 30:
                    raise ValidationError(_("The selected month doesn't have more than 31 days"))
                if month == 2 and day_of_the_month > 28:
                    raise ValidationError(_("February doesn't have more than 28 days"))

