
from odoo import models, api, fields, _
from odoo.exceptions import UserError




class extwiz(models.TransientModel):
    _inherit = "account.payment.register"
    ol_check_in_favor_of = fields.Char('Check in Favor Of')
    
    
    @api.onchange('communication')
    def _compute_check_in_favor_of(self):
        for lines in self.line_ids:
            if lines.student_id.name:
                self.ol_check_in_favor_of = lines.student_id.name
            else:
                invoice=self.env['account.move'].search([])
                for rec in self:
                    for inv in invoice:
                        if rec.communication==inv.name:
                            for lines in inv.invoice_line_ids:
                                if lines.student_id:
                                    student=lines.student_id
                                if student.relationship_ids:
                                    relation=student.relationship_ids
                                    for lines in relation:
                                        if lines.relationship_type_id.name=="Father":
                                            self.ol_check_in_favor_of =lines.individual_id.name
                        else:
                            self.ol_check_in_favor_of = self.partner_id.name


                    
                                  

    @api.model
    def _create_payments(self):
        payments=super(extwiz,self)._create_payments()

        for payment in payments:
            payment.ol_check_in_favor_of = self.partner_id.name
        return payments
class extpayment(models.Model):
    _inherit = "account.payment"
    ol_check_in_favor_of = fields.Char('Check in Favor Of')
