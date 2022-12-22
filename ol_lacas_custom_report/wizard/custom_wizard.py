
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class AccountMoveReport(models.TransientModel):
    _name = 'account.report.move.line'
    
    record_id=fields.Char('ID')
    student_name=fields.Char('Name')
    student_batch=fields.Char('Batch')
    student_branch=fields.Char('Branch')
    withdrawn_status=fields.Char('Withdrawn Status')
    # leaving_reason=fields.Char('Leaving Reason')
    remarks=fields.Char('Remarks')
    withdrawn_date=fields.Char('Withdrawn Date')
    
    
    
    
    
 



class ReceivablesReportWizard(models.TransientModel):
    _name="receivable.report.wizard"
    _description='Print receivable Wizard'

    date_from=fields.Date(string="Date From")
    date_to=fields.Date(string="Date To")

    account_report_line=fields.Many2many('account.report.move.line', string='Account report Line')


    def action_print_report(self):
        bills = self.env['account.move'].search([('state','=','posted'),('refund_receive','=','Receivable')])
        # raise UserError(str(bills))
        lines=[]
        for rec in bills:

            data={
    
                'record_id':rec.name if rec.name else " ",
                'student_name':rec.partner_id.name if rec.partner_id.name else " ",
                'student_batch':rec.x_studio_batch.x_name if rec.x_studio_batch.x_name else " ",
                'student_branch':rec.student_ids.school_ids.name if rec.student_ids.school_ids.name else " " ,
                'withdrawn_status':rec.x_studio_withdrawn_status if rec.x_studio_withdrawn_status else " ",
                # 'leaving_reason':rec.leaving_reason if rec.leaving_reason else " ",
                'remarks':rec.remarks if rec.remarks else " ",
                'withdrawn_date':rec.invoice_date if rec.invoice_date else " ",
                
 
                
      
            }

            mvl=self.env['account.report.move.line'].create(data)
            lines.append(mvl.id)
        self.write({
            "account_report_line":[(6,0,lines)]
        }

        )
        # raise UserError(str(self.account_report_line[0].part_name))

        datalines = []
       

        for record in self.account_report_line:
            datalines.append([record.record_id,record.student_name,record.student_batch,record.student_branch,record.withdrawn_status,record.remarks,record.withdrawn_date])
            # datalines.append([record.student_name])
            # datalines.append([record.student_batch])
            # datalines.append([record.student_branch])
            # datalines.append([record.withdrawn_status])
            # # datalines.append([record.leaving_reason])
            # datalines.append([record.remarks])
            # datalines.append([record.withdrawn_date])
            

        
        data = {
            "datalines" : datalines
        }

            
        # raise UserError(str(bills))

        return self.env.ref('ol_lacas_custom_report.action_report_receivables').report_action(self,data)
      
