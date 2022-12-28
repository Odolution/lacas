
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class GroupAging(models.Model):
    _name = 'aging.invoice.group'

    name  =  fields.Char(string="Name")
    grouping = fields.Char('Groups')

class AccountMoveReport(models.TransientModel):
    _name = 'account.report.move.line'
    
    record_id=fields.Char('ID')
    roll_no=fields.Integer('Roll No')
#     student_name=fields.Char('Name')
    student_batch=fields.Char('Batch')
    student_branch=fields.Char('Branch')
    student_class=fields.Char('Class')
    withdrawn_status=fields.Char('Withdrawn Status')
    leaving_reason=fields.Char('Leaving Reason')
    remarks=fields.Char('Remarks')
    withdrawn_date=fields.Char('Withdrawn Date')
    receivable_amount=fields.Float('Amount Totals')
    footer=fields.Char("Footer")
    total_amount=fields.Float("Total")
    heading=fields.Char('Heading')
    Student=fields.Char('Student')
    Month=fields.Char('Month')

    
   

class ReceivablesReportWizard(models.TransientModel):
    _name="receivable.report.wizard"
    _description='Print receivable Wizard'

    date_from=fields.Date(string="Date From")
    date_to=fields.Date(string="Date To")

    account_report_line=fields.Many2many('account.report.move.line', string='Account report Line')
    groups_ids = fields.Many2many('aging.invoice.group', string='Groups')

    def get_grp_field_value_from_obj(self,grp,obj):
            grpfields=grp.split(".")
            output=obj
            for grpfield in grpfields:
                    
                    output=output[grpfield]
            return output
    
    def recursiveGetData(self,data,appendablelist):
        locallist=[]
        count = 0
        
        # raise UserError(str(data))    
        for key in data.keys():
            val=data[key]

            # if count >0 :
            #     appendablelist.append({
            #             "heading":"Group: "+str(key),
            #             "footer" : True
            #             })

            # if count == 0:
            tpl={
                        "heading":"Student: "+str(key[0]),
                
                  
                        }
            tpl[key[1]]=key[0]
            appendablelist.append(tpl)
                # count += 1
            

            # raise UserError(str(appendablelist))

           
            if type(val)==type(dict()):
                
                val = self.recursiveGetData(val,appendablelist)
                # raise UserError(str(appendablelist))
            
               

            elif type(val)==type(list()):
                count = 0
                for value in val:
                    appendablelist.append({
                            
                    'record_id':value.name if value.name else " ",
                    'roll_no':value.x_student_id_cred.facts_udid if value.x_student_id_cred.facts_udid else 0,
                    'student_batch':value.x_studio_batch.x_name if value.x_studio_batch.x_name else " ",
                    'student_branch':value.x_student_id_cred.school_ids.name if value.x_student_id_cred.school_ids.name else " " ,
                    'student_class':value.x_student_id_cred.homeroom if value.x_student_id_cred.homeroom else " " ,
                    'withdrawn_status':value.x_studio_withdrawn_status if value.x_studio_withdrawn_status else " ",
                    'leaving_reason':value.leaving_reason.name if value.leaving_reason.name else " ",
                    'remarks':value.remarks if value.remarks else " ",
                    'withdrawn_date':value.invoice_date if value.invoice_date else " ",
                    'receivable_amount': value.amount_residual if value.amount_residual else 0,
                                })
                

            else:
                print("invalid datatype ")
                # raise UserError("invalid datatype : "+str(val))
            sum=0
            for value in val:
                locallist.append(value)
                sum+=value.amount_residual
            tpl={
                            
                    "footer":"Total: "+str(key[0]),
                    'total_amount': sum,
                                }
            
            tpl[key[1]]=key[0]
            appendablelist.append(tpl)


            
        return locallist


    def action_print_report(self):
       
        #creating dynamic filters
 

        move_ids=self.env['account.move'].search([('move_type','=','out_refund'),('state','=','posted'),('payment_state','=','not_paid'),('refund_receive','=','Receivable'),("invoice_date",">=",self.date_from),("invoice_date","<=",self.date_to)])
        # for rec in move_ids:
        #     raise UserError(rec.name)
        if self.groups_ids:

            dict_data={}
            for mov in move_ids:
                data=dict_data
                group_lst = []
                for grp in self.groups_ids:
                    ans=self.get_grp_field_value_from_obj(grp.grouping,mov)
                    group_lst.append((ans,grp.name))
                
                for grp in group_lst[:-1]:
                        tempdata=data.get(grp,None)
                        if tempdata==None:
                            data[grp]={}
                            tempdata=data[grp]
                        data=tempdata
                grp=group_lst[-1]
                tempdata=data.get(grp,None)
                if tempdata==None:
                    data[grp]=[]
                    
                data[grp].append(mov)
            

            
            datalist=[]    
                                                   ##this list hold objects that need to be created
            final_list=self.recursiveGetData(dict_data,datalist)         #this list holds items for final sum
            
            
            
           
            
            # creating line in aging.invoice.line
            lines=[]
            for data in datalist:

                mvl=self.env['account.report.move.line'].create(data)
                lines.append(mvl.id)
            
            
        self.write({
            "account_report_line":[(6,0,lines)]
        }

        )
        
            

        datalines = []
                

        for rec in self.account_report_line:
            
                
            # datalines.append([record.get('heading'," "),record.get('record_id'," "),record.get('receivable_amount',''),record.get('footer'," "),record.get('total_amount','')])
            datalines.append([rec.heading,rec.Month,rec.Student,rec.record_id,rec.receivable_amount,rec.footer,rec.total_amount,rec.roll_no,rec.student_batch,rec.student_branch,rec.student_class,rec.withdrawn_status,rec.leaving_reason,rec.remarks,rec.withdrawn_date])

                                                                                  
            
        # 

        # raise UserError(str(datalines))
        data = {
            "datalines" : datalines}

        
        
        
          

        
    
        
        return self.env.ref('ol_lacas_custom_report.action_report_receivables').report_action(self,data)


































      
       # bills = self.env['account.move'].search([('move_type','=','out_refund'),('state','=','posted'),('refund_receive','=','Receivable'),('payment_state','=','not_paid')])
        # # raise UserError(str(bills))
        # lines=[]
        # for rec in bills:

        #     data={
    
        #         'record_id':rec.name if rec.name else " ",
        #         'student_name':rec.partner_id.name if rec.partner_id.name else " ",
        #         'student_batch':rec.x_studio_batch.x_name if rec.x_studio_batch.x_name else " ",
        #         'student_branch':rec.x_student_id_cred.school_ids.name if rec.x_student_id_cred.school_ids.name else " " ,
        #         'student_class':rec.x_student_id_cred.homeroom if rec.x_student_id_cred.homeroom else " " ,
        #         'withdrawn_status':rec.x_studio_withdrawn_status if rec.x_studio_withdrawn_status else " ",
        #         'leaving_reason':rec.leaving_reason.name if rec.leaving_reason.name else " ",
        #         'remarks':rec.remarks if rec.remarks else " ",
        #         'withdrawn_date':rec.invoice_date if rec.invoice_date else " ",
                
 
                
      
        #     }

        #     mvl=self.env['account.report.move.line'].create(data)
        #     lines.append(mvl.id)
