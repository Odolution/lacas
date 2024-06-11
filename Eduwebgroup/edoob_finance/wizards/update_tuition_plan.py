# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
import datetime

import logging

_logger = logging.getLogger(__name__)


class UpdateTuitionPLan(models.TransientModel):
    _name = 'update.tuition.plan'
    _description = "Update tuition plan"

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'tuition_plan_ids' in fields_list and self._context.get('active_model', False) == 'tuition.plan':
            res['tuition_plan_ids'] = self._context.get('active_ids', [])
        return res

    tuition_plan_ids = fields.Many2many(
        'tuition.plan', required=True, string="Tuition plans")

    update_installments = fields.Boolean(string="Update installments", default=True)
    update_lines = fields.Boolean(string="Update lines", default=True)

    update_invoice_method = fields.Boolean(string="Update invoice method", default=True)
    update_post_action_option = fields.Boolean(string="Update post action option", default=True)
    update_pricelist_option = fields.Boolean(string="Update pricelist option", default=True)

    update_company_id = fields.Boolean(string="Update company", default=True)
    update_currency_id = fields.Boolean(string="Update currency", default=True)
    update_journal_id = fields.Boolean(string="Update journal", default=True)

    update_fiscal_position_id = fields.Boolean(string="Update fiscal position", default=True)
    update_analytic_account_id = fields.Boolean(string="Update analytic account", default=True)

    def _prepare_plan_values_to_write(self, template):
        values_to_write = {}
        if self.update_invoice_method:
            values_to_write['invoice_method'] = template.invoice_method
        if self.update_post_action_option:
            values_to_write['post_action_option'] = template.post_action_option
        if self.update_pricelist_option:
            values_to_write['pricelist_option'] = template.pricelist_option
        if self.update_company_id:
            values_to_write['company_id'] = template.company_id.id
        if self.update_currency_id:
            values_to_write['currency_id'] = template.currency_id.id
        if self.update_journal_id:
            values_to_write['journal_id'] = template.journal_id.id
        if self.update_fiscal_position_id:
            values_to_write['fiscal_position_id'] = template.fiscal_position_id.id
        if self.update_analytic_account_id:
            values_to_write['analytic_account_id'] = template.analytic_account_id.id
        return values_to_write

    def button_update_tuition_plans(self):
        self.ensure_one()
        tuition_templates = self.mapped('tuition_plan_ids.tuition_template_id')
        plans_by_template = [
            (template, self.tuition_plan_ids.filtered(lambda tp: tp.tuition_template_id == template))
            for template in tuition_templates]
        for template, plans in plans_by_template:
            values_to_write = self._prepare_plan_values_to_write(template)
            if values_to_write:
                for plan in plans:
                    plan_name = plan.name
                    plan_id = plan.id
                    try:
                        if self.update_installments:
                            plan.set_installments_to_template()
                            plan._compute_next_installment()
                        if self.update_installments:
                            plan.set_lines_to_template()
                        plan.write(values_to_write)
                    except Exception as e:
                        now = datetime.datetime.now()
                        msg = _("An error has occurred during the update of the tuition plan[%s]: %s\n"
                                "\nError message: %s\nError time: %s\n"
                                "Please, contact with your administrator.",
                                plan_id, plan_name, e, now)
                        _logger.error(e)
                        raise UserError(msg)
