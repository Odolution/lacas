import string
from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class credit_notes_fields(models.Model):
    _inherit = "account.move"
    withdrawl_submission_date = fields.Date(string="Withdrawal Submission")
    actual_leaving_date = fields.Date(string="Leaving Date")
    notice_completion_date = fields.Date(string="Notice Completion")
    # school_branch = fields.Char(string="Branch")
    # class_grade = fields.Char(string="Class")
    # Roll_no = fields.Char(string="Roll No")
    # Student_id = fields.Char(string="Student")

    @api.onchange('withdrawl_submission_date')
    def _one_month_after(self):

        if self.withdrawl_submission_date:
            self.notice_completion_date = self.withdrawl_submission_date + \
                relativedelta(months=1)


# class report_sale_preview(models.Model):
#     _inherit = 'sale.order'
#     preview = fields.Html('Report Preview')

#     def generate_preview(self):
#         # html = self.env['ir.actions.report'].get_html(
#         #     self, 'sale.report_saleorder')
#         data_format = self.env.ref('sale.report_saleorder')
#         self.write({'preview': data_format})
#         return True
