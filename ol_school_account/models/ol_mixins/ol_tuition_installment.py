# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons.account.models.company import MONTH_SELECTION
from dateutil.relativedelta import relativedelta
from odoo.tools import format_datetime
from datetime import datetime
from odoo.tools import html2plaintext, is_html_empty, plaintext2html, DEFAULT_SERVER_DATETIME_FORMAT as dtf
from odoo.tools.misc import get_lang

# tuition.installmen.mixin 

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

# tuition.plane.line.mixin 

class TuitionPlanLineMixin(models.AbstractModel):
    _inherit = 'mail.thread'
    _name = 'tuition.line.mixin'
    _description = "Tuition line mixin"
    _order = 'sequence'

    sequence = fields.Integer("Sequence")
    name = fields.Char("Description", required=True)
    product_id = fields.Many2one('product.product', string="Product", required=True, ondelete='restrict')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
    product_uom_category_id = fields.Many2one('uom.category', related='product_id.uom_id.category_id')

    account_id = fields.Many2one(
        'account.account', string='Account',
        index=True, ondelete="cascade",
        domain="[('deprecated', '=', False), ('company_id', '=', 'company_id'),('is_off_balance', '=', False)]",
        check_company=True,
        tracking=True)
    journal_id = fields.Many2one('account.journal', string="Journal", domain="[('type', '=', 'sale')]")
    quantity = fields.Float("Quantity", default=1.0, digits='Product Unit of Measure')
    currency_id = fields.Many2one('res.currency', string="Currency", required=True)
    unit_price = fields.Monetary("Unit price")
    tax_ids = fields.Many2many('account.tax', string="Taxes")

    discount = fields.Float("Discount", digits='Discount', default=0.0)

    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)
    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account',
        index=True, compute_sudo='_compute_analytic_fields', store=True, readonly=False, check_company=True, copy=True)
    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag', string='Analytic Tags', compute_sudo='_compute_analytic_fields',
        store=True, readonly=False, check_company=True, copy=True)

    @api.depends('quantity', 'discount', 'unit_price', 'tax_ids')
    def _compute_amount(self):
        """ Compute the amounts of the SO line. """
        for line in self:
            price = line.unit_price * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.currency_id, line.quantity, product=line.product_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_ids.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_ids.id])

    @api.depends('product_id', 'account_id')
    def _compute_analytic_fields(self):
        for line in self:
            rec = self.env['account.analytic.default'].account_get(
                product_id=line.product_id.id,
                account_id=line.account_id.id,
                user_id=line.env.uid,
                date=fields.Date.today(),
                company_id=self.env.company.id,
            )
            line.analytic_account_id = rec.analytic_id
            line.analytic_tag_ids = rec.analytic_tag_ids

# tuition.plan.mixin

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
        default=lambda self: self.env.ref('ol_school_account.sale_mail_template_id'))
    invoice_mail_template_id = fields.Many2one(
        'mail.template', string="Invoice mail template", required=True,
        default=lambda self: self.env.ref('ol_school_account.invoice_mail_template_id'))
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