from odoo import models, fields, api
from odoo.exceptions import UserError


class account_fields(models.Model):
    _inherit = "account.move"
    room = fields.Char("Class")

    photograph_charges = fields.Char("Photograph Charges")
    student_security = fields.Char("Student Security")
    admission_fee = fields.Char("Admission Fee")
    father_name = fields.Char("Father Name")
    start_session = fields.Date("Start Session")
    end_session = fields.Date("End Session")
    Registration_id = fields.Char("Registration ID")
    discount_note = fields.Char("Add Discount note")

    reject_reason = fields.Selection(
        [('siblings', 'Siblings Discount'), ('Scholarship', 'Scholarship Discount'), ], 'Reason For Discount')
    
    @api.onchange('state')
    def _onchange_appy_seq(self):
        record = self

        if record.state == 'posted':
          if record.move_type == 'out_invoice':
            record['name'] = 'Draft'
            if 'Draft' in record.name:
              # raise UserError(record)
              if record.school_ids:
                for school in record.school_ids:
                  school_code = school.description
              new_no = school_code + env['ir.sequence'].next_by_code('adm_challan')
              record.sudo().write({
                'name': new_no,
              })
              for rec in record.invoice_line_ids:
                rec['name'] = new_no
          if record.move_type == 'out_refund':
            record['name'] = 'Draft'
            if 'Draft' in record.name:
              # raise UserError(record)
              if record.x_school_id_cred:
                new_no = record.x_school_id_cred.description + env['ir.sequence'].next_by_code('security')
                record.sudo().write({
                  'name': new_no,
                })
                for rec in record.invoice_line_ids:
                  rec['name'] = new_no
              # raise UserError(new_no)


# class school_panel_field(models.Model):
#     _inherit = "school.student"

#     Home_room = fields.Char("HomeRoom")
