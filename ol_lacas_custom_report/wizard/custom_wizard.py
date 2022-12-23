
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class AccountMoveReport(models.TransientModel):
    _name = 'account.report.move.line'
    
    record_id=fields.Char('ID')
    student_name=fields.Char('Name')
    student_batch=fields.Char('Batch')
    student_branch=fields.Char('Branch')
    student_class=fields.Char('Class')
    withdrawn_status=fields.Char('Withdrawn Status')
    leaving_reason=fields.Char('Leaving Reason')
    remarks=fields.Char('Remarks')
    withdrawn_date=fields.Char('Withdrawn Date')
    
   

class ReceivablesReportWizard(models.TransientModel):
    _name="receivable.report.wizard"
    _description='Print receivable Wizard'

    date_from=fields.Date(string="Date From")
    date_to=fields.Date(string="Date To")

    account_report_line=fields.Many2many('account.report.move.line', string='Account report Line')


    def action_print_report(self):
        domain=[]
        date_from=self.date_from
        if date_from:
            domain+=[('invoice_date','>=',date_from)]

        date_to=self.date_to
        if date_to:
            domain+=[('invoice_date','<=',date_to)]
            
        bills = self.env['account.move'].search([('move_type','=','out_refund'),('state','=','posted'),('refund_receive','=','Receivable'),('payment_state','=','not_paid'),(domain])
        # raise UserError(str(bills))
        lines=[]
        for rec in bills:

            data={
    
                'record_id':rec.name if rec.name else " ",
                'student_name':rec.partner_id.name if rec.partner_id.name else " ",
                'student_batch':rec.x_studio_batch.x_name if rec.x_studio_batch.x_name else " ",
                'student_branch':rec.x_student_id_cred.school_ids.name if rec.x_student_id_cred.school_ids.name else " " ,
                'student_class':rec.x_student_id_cred.homeroom if rec.x_student_id_cred.homeroom else " " ,
                'withdrawn_status':rec.x_studio_withdrawn_status if rec.x_studio_withdrawn_status else " ",
                'leaving_reason':rec.leaving_reason.name if rec.leaving_reason.name else " ",
                'remarks':rec.remarks if rec.remarks else " ",
                'withdrawn_date':rec.invoice_date if rec.invoice_date else " ",
                
 
                
      
            }

            mvl=self.env['account.report.move.line'].create(data)
            lines.append(mvl.id)
        self.write({
            "account_report_line":[(6,0,lines)]
        }

        )
       
        datalines = []
       

        for record in self.account_report_line:
            datalines.append([record.record_id,record.student_name,record.student_batch,record.student_branch,record.student_class,record.withdrawn_status,record.leaving_reason,record.remarks,record.withdrawn_date])
          
            

        
        data = {
            "datalines" : datalines
        }

    

        return self.env.ref('ol_lacas_custom_report.action_report_receivables').report_action(self,data)
      
