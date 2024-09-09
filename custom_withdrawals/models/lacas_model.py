from odoo import api, fields, models, _


class academics_tab(models.Model):

    _inherit = 'account.move'
    olf_id_cred_custom = fields.Char(string='olf Id')

    udid_cred_custom = fields.Char(string='UDID',compute='_student_compute_udid')
    acadamic_status = fields.Char( string='Status')

    rollno_cred_custom = fields.Char(string='Roll No')
    remarks_cred_custom = fields.Char(string='REMARKS')
    relationship_cred_custom = fields.Selection([('Father', 'Father'), ('Mother', 'Mother'), ('Uncle', 'Uncle'), ('Aunt', 'Aunt'), ('Brother', 'Brother'), (
        'Sister', 'Sister'), ('Grandparent', 'Grandparent'), ('Friend', 'Friend'), ('Guardian', 'Guardian'), ('Other', 'Other')], string="Relation With Student")
    financial_responsibilty_cred_custom = fields.Selection(
        [('Yes', 'Yes'), ('No', 'No')], string="Financial Responsibilty")
    
    notice_fee_withdrawal = fields.Monetary(compute='_compute_notice_fee', string="Notice Fee")
    amount_total_withdrawal = fields.Monetary(compute='_compute_total_amount', string="Total Withdrawal")
    refund_receive = fields.Char(
        compute='_compute_refund_receive', string="Receivable/Refundable")
    

    # @api.onchange('x_student_id_cred')
    def _student_compute_udid(self):
        for rec in self:
            rec.udid_cred_custom=""
            if rec.x_student_id_cred:
                rec.udid_cred_custom=rec.x_student_id_cred.olf_udid
    
    def _compute_notice_fee(self):
        # if self.move_type == "out_refund":
        for rec in self:
            rec.notice_fee_withdrawal = 0
            rec.x_studio_withdrawn_status = 'N'  
            
            if rec.x_studio_charges:
                total_custom = 0
                for inv_line in rec.x_studio_charges.invoice_line_ids:
                    total_custom = inv_line.price_subtotal+total_custom
                rec.notice_fee_withdrawal = total_custom
          
                
            if rec.payment_state == 'paid':
                rec.x_studio_withdrawn_status = 'Y'
            
                                                                                                                                                              


    def _compute_total_amount(self):
        for rec in self:
            if rec.invoice_line_ids:
                rec.amount_total_withdrawal = abs(rec.notice_fee_withdrawal- rec.amount_total)
                # for cred in rec.invoice_line_ids:
                #     rec.amount_total_withdrawal = abs(rec.notice_fee_withdrawal-cred.price_subtotal)
            else:
                rec.amount_total_withdrawal = 0



    def _compute_refund_receive(self):
        for rec in self:
            receive = 0
            refund = 0
            if rec.x_studio_charges:

                if rec.x_studio_charges.invoice_line_ids:

                    for i in rec.x_studio_charges.invoice_line_ids:
                        #refund = i.price_subtotal
                        receive += i.price_subtotal
                if self.invoice_line_ids:
                    for j in rec.invoice_line_ids:
                        #receive = j.price_subtotal
                        refund += j.price_subtotal

                if receive > refund:
                    rec.refund_receive = 'Receivable'
                elif receive == refund:
                    rec.refund_receive = 'Receivable'
                else:
                    rec.refund_receive = 'Refundable'
            else:
                rec.refund_receive = 'Refundable'

        # if self.x_studio_charges:

        #     if self.x_studio_charges.invoice_line_ids:

        #         for i in self.x_studio_charges.invoice_line_ids:
        #             refund = i.price_subtotal
        #     if self.invoice_line_ids:
        #         for j in self.invoice_line_ids:
        #             receive = j.price_subtotal

        #     if receive > refund:
        #         self.refund_receive = 'Receivable'
        #     else:
        #         self.refund_receive = 'Refundable'
        # else:
        #     self.refund_receive = 'Refundable'

#   record.write({'x_receivable_refundable': 'receivable'})
