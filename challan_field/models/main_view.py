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
    father_facts_id=fields.Char('Father Facts ID')
    security_amnt_lv=fields.Integer("Secuirity Amount")
    other_refunds_lv=fields.Integer("Other Refunds")
    

    class_name = fields.Char(string='Class')
    section_name = fields.Char(string='Section')
    @api.onchange('x_student_id_cred',"student_ids")
    def _student_onchange(self):
      self.class_name=""
      self.section_name=""
      self.father_name=""
      self.security_amnt_lv=0
      self.other_refunds_lv=0
      ##work for class and section picking
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

      if self.invoice_line_ids:
        for line_inv in self.invoice_line_ids:
          if line_inv.product_id.id==83:
            self.security_amnt_lv=line_inv.price_total
          if line_inv.product_id.id==408:
            self.other_refunds_lv=line_inv.price_total

        ##work for father name picking
        for relation in self.x_student_id_cred.relationship_ids:
          if relation.relationship_type_id.name == "Father":
            self.father_facts_id=relation.individual_id.facts_id
            self.father_name = relation.individual_id.name
            break
      
      for student in self['student_ids']:
         wholename=""
         if student.homeroom:
             wholename=student.homeroom
             splitted_name=wholename.split('-')
             if len(splitted_name)>2:
                self.class_name=splitted_name[0]+"-"+splitted_name[1]
                self.section_name=splitted_name[2]
             elif len(splitted_name)>1:
                self.class_name=splitted_name[0]
                self.section_name=splitted_name[1]
             elif len(splitted_name)>0:
                self.class_name=splitted_name[0]
         ##work for father name picking
         for relation in student['relationship_ids']:
            if relation['relationship_type_id']['name'] == "Father":
              self['father_name'] = relation['individual_id']['name']
              break
         break
            
        
#     @api.onchange('state')
    def action_post(self):
#         record = self
        for rec in self:
            seq = 1
            if '/' in rec.name:
                seq = 0
#             raise UserError(rec.name)
        res = super(account_fields, self).action_post()
        for record in self:
#             raise UserError(record.name)
            if record.state == 'posted':
              if record.move_type == 'out_invoice':
#                 record['name'] = 'Draft'
                
                if seq == 0:
                  
                  school_code=""
                  if record.school_ids:
                    for school in record.school_ids:
                      school_code = school.description
                  if record.x_school_id_cred:
                    for school in record.x_school_id_cred:
                      school_code = school.description
                 # new_no = school_code + record.env['ir.sequence'].next_by_code('adm_challan')
                  if record.journal_id.id == 119:
                    new_no = school_code + record.env['ir.sequence'].next_by_code('adm_challan')
                    rec['name']=new_no
                  if record.journal_id.id == 125:
                    new_no = school_code + record.env['ir.sequence'].next_by_code('monthly_bills')
                    rec['name']=new_no
                  if record.journal_id.id == 126:
                    new_no = school_code + record.env['ir.sequence'].next_by_code('bi_monthly')
                    rec['name']=new_no
                    
                  #record.name = new_no
                  if record.journal_id.id == 124:
                    new_no = record.env['ir.sequence'].next_by_code('charges_reversal')
                    rec['name']=new_no  
                    #record.name = new_no
                    
                  for rec in record.line_ids:
                    #raise UserError(rec.new_no)  
                    new_no=rec['name']
                    record.payment_reference = new_no
                    
              if record.move_type == 'out_refund':
#                 record['name'] = 'Draft'
                if seq == 0:
                  # raise UserError(record)
                  if record.x_school_id_cred:
                    new_no = record.x_school_id_cred.description + record.env['ir.sequence'].next_by_code('security')
                    record.payment_reference = new_no
                    record.name = new_no
                    
                    for rec in record.line_ids:
                      rec['name'] = new_no
        return res
                  # raise UserError(new_no)


# class school_panel_field(models.Model):
#     _inherit = "school.student"

#     Home_room = fields.Char("HomeRoom")
