from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import datetime, base64
import threading

class ChallanPrinting(models.Model):
    _name = 'challan.printing'
    _description = 'Challan Printing'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    branch_ids = fields.Many2many('school.school', string='Branch')
    class_ids = fields.Many2many('school.grade.level', string='Class')
    journal_id = fields.Many2one('account.journal', string='Journal')
    enrollment_status_ids = fields.Many2many('school.enrollment.status', string='Enrollment Status')


    @api.depends('from_date', 'to_date')
    def _compute_name(self):
        for rec in self:
            name = []
            if rec.from_date: name.append(str(rec.from_date))
            if rec.to_date: name.append(str(rec.to_date))
            rec.name = ' - '.join(name)


    def _get_sorted_bill_ids(self, unordered_bills):
        ''' Function to Sort the Bills '''
        grade_levels = {
            "R": 0,
            "PG": 1,
            "PR": 2,
            "N":3,
            "NUR":4,
            # "R": 4,
            "KG": 5,
            "I": 6,
            "II": 7,
            "III": 8,
            "IV": 9,
            "V": 10,
            "VI": 11,
            "VII": 12,
            "VIII": 13,
            "IX": 14,
            "X": 15,
            "A-I": 16,
            "A-II": 17
        }

        sorted_bills = sorted(unordered_bills, key=lambda x: (grade_levels.get(x.class_name, 9999), x['section_name'] or 'z', x['student_ids']['first_name'], x['student_ids']['last_name']))
        sorted_bill_ids = []
        for i in sorted_bills:
            sorted_bill_ids.append(i.id)
        
        return sorted_bill_ids


    def _generate_challan_pdf(self):
        ''' Generate PDF Challan and attach to the attachment '''
        self.ensure_one()

        # create a new cursor to access database and change the environment accordingly
        new_cr = self.pool.cursor()
        self = self.with_env(self.env(cr=new_cr))

        # search and sort the bills
        domain = [
            ('move_type', '=', 'out_invoice'),
            ('invoice_date', '>=', self.from_date ),
            ('invoice_date', '<=', self.to_date ),
            ('x_studio_previous_branch', 'in', self.branch_ids.mapped('name') ),
            ('x_studio_previous_class', 'in', self.class_ids.mapped('name') ),
            ('journal_id', '=', self.journal_id.id ),
            ('x_studio_enrollment_statusbills', 'in', self.enrollment_status_ids.ids ),
            ('state', '=', 'posted'),
            ('payment_state', '=', 'not_paid')
        ]
        # bills = self.env['account.move'].browse([380071,380067,380061,380056,380050,380036,380031,380021,380010,379989,379986,379984,379978,379970,379969])
        bills = self.env['account.move'].search(domain)
        sorted_bill_ids = self._get_sorted_bill_ids(bills)

        # render pdf data and encode in bytes
        report = self.env.ref('cus_report.report_fee_challan_students_initiate')._render_qweb_pdf(sorted_bill_ids)[0]
        pdf_attachment = base64.b64encode(report)

        # create attachment for the PDF and attach in the record
        attachment = self.env['ir.attachment'].create({
            'name': f'Students Challan ({self.name}).pdf',
            'type': 'binary',
            'datas': pdf_attachment,
            'store_fname': f'Students Challan ({self.name}).pdf',
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        # commit the changes to the database
        new_cr.commit()

        # close the cursor to disconnect connection to database
        # else database will disconnect and mark it as trash connection
        new_cr.close()

        return {}


    def generate_challan_pdf(self):
        self.ensure_one()

        if not (self.from_date and self.to_date and self.branch_ids and self.journal_id and self.enrollment_status_ids):
            raise UserError('Please Set all the values')

        # create threads to run function that will create its own connection to database
        threaded_calculation = threading.Thread(
            target = self._generate_challan_pdf,
            args = ()
        )
        threaded_calculation.start()
