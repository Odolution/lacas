from odoo import models, fields, api
from odoo.exceptions import UserError



class reason_for_discount(models.Model):
    _name="discount.reason"
    name = fields.Char('name')
class reason_for_leave(models.Model):
    _name="leaving.reason"
    name = fields.Char('name')

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
    reject_reason = fields.Many2one('discount.reason', string='Reason For Discount')
    leaving_reason = fields.Many2one("leaving.reason", string = "Leaving Reason")
    remarks = fields.Char('remarks')

    class_name = fields.Char(string='Class')
    section_name = fields.Char(string='Section')
    @api.onchange('x_student_id_cred')
    def _student_onchange(self):
      self.class_name=""
      self.section_name=""
      if self.x_student_id_cred:
        wholename=""
        if self.x_student_id_cred.homeroom:
          wholename=self.x_student_id_cred.homeroom
          splitted_name=wholename.split('-')
          if len(splitted_name)>2:
            self.class_name=splitted_name[0]+"-"+splitted_name[1]
            self.section_name=splitted_name[2]
          elif len(splitted_name)>1:
            self.class_name=splitted_name[0]
            self.section_name=splitted_name[1]
          elif len(splitted_name)>0:
            self.class_name=splitted_name[0]
        
    @api.onchange('state')
    def _onchange_appy_seq(self):
        record = self

        if record.state == 'posted':
          if record.move_type == 'out_invoice':
            record['name'] = 'Draft'
            if 'Draft' in record.name:
              # raise UserError(record)
              school_code=""
              if record.school_ids:
                for school in record.school_ids:
                  school_code = school.description
              if record.x_school_id_cred:
                for school in record.x_school_id_cred:
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
