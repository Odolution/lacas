# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class TuitionPlanMixin(models.AbstractModel):
    _name = 'tuition.plan.mixin'
    _description = "Tuition mixin"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    @api.model
    def _get_default_journal(self):
        return self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()

    @api.model
    def _default_pricelist_id(self):
        return self.env['product.pricelist'].search(['|', ('company_id', '=', False), ('company_id', '=', self.env.company.id)], limit=1)

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, required=True)
    journal_id = fields.Many2one(
        'account.journal', required=True, string="Default journal", domain="[('type', '=', 'sale')]",
        default=_get_default_journal)

    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position',
        domain="[('company_id', '=', company_id)]", check_company=True,
        help="Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices."
             "The default value comes from the customer.")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic account")
    tax_country_id = fields.Many2one(
        'res.country', compute='_compute_tax_country_id',
        help="Technical field to filter the available taxes depending on the fiscal country and fiscal position.")

    sale_mail_template_id = fields.Many2one(
        'mail.template', string="Sale order/quotation mail template", required=True,
        default=lambda self: self.env.ref('edoob_finance.sale_mail_template_id'))
    invoice_mail_template_id = fields.Many2one(
        'mail.template', string="Invoice mail template", required=True,
        default=lambda self: self.env.ref('edoob_finance.invoice_mail_template_id'))
    terms_type = fields.Selection(related='company_id.terms_type')
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment terms', check_company=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    program_id = fields.Many2one(
        'school.program', required=True, ondelete='restrict', default=lambda self: self.env.program,
        domain="[('school_id.district_company_ids', '=', company_id)]")

    invoice_method = fields.Selection(selection=[
        ('sale', 'Sale order'),
        ('move', 'Invoice'),
        ], default='sale', required=True)
    post_action_option = fields.Selection(selection=[
        ('nothing', "Do nothing"),
        ('send', "Send"),
        ('confirm', "Confirm"),
        ('confirm_send', "Confirm & send"),
        ], default='confirm_send', required=True, string="Post-action option")

    pricelist_option = fields.Selection(
        selection=[
            ('fixed_prices', "Fixed prices"),
            ('invoice_address', "Invoice address"),
            ('student', "Student"),
            ('fixed_pricelist', "Fixed pricelist"),
            ], default='fixed_prices', required=True)
    pricelist_id = fields.Many2one('product.pricelist', default=_default_pricelist_id)

    @api.constrains('invoice_method', 'post_action_option')
    def check_invoice_should_be_posted_before_sent(self):
        for record in self:
            if record.invoice_method == 'move' and record.post_action_option == 'send':
                raise UserError(_("You cannot use the post-action option 'send' if you are using the invoice mode.\nInvoices should be posted before being sent."))

    @api.depends('company_id.account_fiscal_country_id', 'fiscal_position_id.country_id', 'fiscal_position_id.foreign_vat')
    def _compute_tax_country_id(self):
        for record in self:
            if record.fiscal_position_id.foreign_vat:
                record.tax_country_id = record.fiscal_position_id.country_id
            else:
                record.tax_country_id = record.company_id.account_fiscal_country_id
