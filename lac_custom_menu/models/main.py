from odoo import models, api, fields, _
from odoo.exceptions import UserError

class field_changes_custom_update(models.Model):
    _inherit = 'account.move'
    udid_new_lv = fields.Char(compute='_compute_udid_student',string="UDID")
    facts_id_new_lv = fields.Char(compute='_compute_facts_id_student',string="Facts Id")
    adm_amount=fields.Monetary(string="Admission Amount",compute="_onchange_adm_amount_data")
    security_amount=fields.Monetary(string="Security Amount",compute="_onchange_security_amount_data")


    @api.onchange('student_ids')
    def _onchange_adm_amount_data(self):
        self._get_adm_amt_field()

    @api.onchange('invoice_line_ids')
    def _onchange_adm_amount_data(self):
        self._get_adm_amt_field()

    def _get_adm_amt_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.adm_amount=0
        for rec in adm_journals:
            if rec.invoice_line_ids: 
                    for line in rec.invoice_line_ids:
                        if 'Admission' in line.product_id.name:
                            rec['adm_amount']=line.price_subtotal

    @api.onchange('invoice_line_ids')
    def _onchange_security_amount_data(self):
        self._get_sec_amt_field()
    
                
    def _get_sec_amt_field(self):
        adm_journal=self.env['account.journal'].search([('code','=','ADM')])
        adm_journals=self.env['account.move'].search([('journal_id','=',adm_journal.id)])
        self.security_amount=''
        for rec in adm_journals:
             if rec.invoice_line_ids: 
                    for line in rec.invoice_line_ids:
                        if 'Security' in line.product_id.name:
                            rec['security_amount']=line.price_subtotal

    
    def _compute_udid_student(self):
        # if self.move_type == "out_refund":
        for rec in self:
            if rec.student_ids:
                for stu_rec in rec.student_ids:
                    rec.udid_new_lv=stu_rec.facts_udid
            else:
                rec.udid_new_lv=""

            # for rec in self:
            # if rec.tuition_plan_ids:
            #     for stu_rec in rec.tuition_plan_ids:
            #         rec.udid_new_lv=stu_rec.student_id.facts_udid
            # else:
            #     rec.udid_new_lv=""

    def _compute_facts_id_student(self):
        # if self.move_type == "out_refund":
        for rec in self:
            if rec.student_ids:
                for stu_rec in rec.student_ids:
                    rec.facts_id_new_lv=stu_rec.facts_id
            else:
                rec.facts_id_new_lv=""
