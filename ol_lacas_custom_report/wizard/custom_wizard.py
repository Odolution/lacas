
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class AccountMoveReport(models.TransientModel):
    _name = 'account.report.move.line'

    part_name=fields.Char('Name')
 



class ReceivablesReportWizard(models.TransientModel):
    _name="receivable.report.wizard"
    _description='Print receivable Wizard'

    date_from=fields.Date(string="Date From")
    date_to=fields.Date(string="Date To")

    account_report_line=fields.Many2many('account.report.move.line', string='Account report Line')


    def action_print_report(self):
        bills = self.env['account.move'].search([('move_type','=','out_refund')])
        # raise UserError(str(bills))
        lines=[]
        for rec in bills:

            data={
                'part_name':rec.partner_id.name,
                

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
            datalines.append([record.part_name])

        
        data = {
            "datalines" : datalines
        }

            
        # raise UserError(str(bills))

        return self.env.ref('ol_lacas_custom_report.action_report_receivables').report_action(self,data)
      