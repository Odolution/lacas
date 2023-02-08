import string
from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class credit_notes_fields(models.Model):
    _inherit = "account.move"
    withdrawl_submission_date = fields.Date(string="Withdrawal Submission")
    actual_leaving_date = fields.Date(string="Leaving Date")
    notice_completion_date = fields.Date(string="Notice Completion")
    next_month_Date=fields.Date(string="next month date")
    next_month=fields.Char(string="next month ",compute="_get_next_month")

    # school_branch = fields.Char(string="Branch")
    # class_grade = fields.Char(string="Class")
    # Roll_no = fields.Char(string="Roll No")
    # Student_id = fields.Char(string="Student")

    @api.onchange('withdrawl_submission_date')
    def _one_month_after(self):

        if self.withdrawl_submission_date:
            self.notice_completion_date = self.withdrawl_submission_date + \
                relativedelta(months=1)

    @api.onchange('create_date')
    def _next_month(self):

        if self.create_date:
            self.next_month_Date = self.create_date + \
                relativedelta(months=1)

    def _get_next_month(self):
        self.next_month=''
        for rec in self:
            create_on_date=str(rec.create_date)
            splitted_name=create_on_date.split('-')
            if len(splitted_name)>2:
                month_in_number=splitted_name[1]
                if month_in_number == '12':
                    rec['next_month']='December'
                elif month_in_number == '11':
                    rec['next_month']='November'
                elif month_in_number == '10':
                    rec['next_month']='October'
                elif month_in_number == '09':
                    rec['next_month']='September'
                elif month_in_number == '08':
                    rec['next_month']='August'
                elif month_in_number == '07':
                    rec['next_month']='July'
                elif month_in_number == '06':
                    rec['next_month']='June'
                elif month_in_number == '05':
                    rec['next_month']='May'
                elif month_in_number == '04':
                    rec['next_month']='April'
                elif month_in_number == '03':
                    rec['next_month']='March'
                elif month_in_number == '02':
                    rec['next_month']='Feburary'
                elif month_in_number == '01':
                    rec['next_month']='January'



# class report_sale_preview(models.Model):
#     _inherit = 'sale.order'
#     preview = fields.Html('Report Preview')

#     def generate_preview(self):
#         # html = self.env['ir.actions.report'].get_html(
#         #     self, 'sale.report_saleorder')
#         data_format = self.env.ref('sale.report_saleorder')
#         self.write({'preview': data_format})
#         return True
