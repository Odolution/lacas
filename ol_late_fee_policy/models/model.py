
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime

class late_fee_slab(models.Model):
    _name = "account.latefeeslab"
    days = fields.Integer('Days')
    charge = fields.Float('Charge')

class payment_ext(models.Model):
    _inherit = "account.payment"
    late_fee=fields.Float(string="Late Fee")   
    amount_late_fee_exclusive=fields.Float(string="Total without Late Fee")
class extwiz(models.TransientModel):
    _inherit = "account.payment.register"
    late_fee=fields.Float(string="Late Fee",compute='_compute_late_fee')
    amount_late_fee_exclusive=fields.Float(string="Total without Late Fee",compute='_compute_late_fee')
    def _compute_late_fee(self):
        for wizard in self:
            invoice=""
            wizard.late_fee=0
            for line in wizard.line_ids:
                invoice=line.move_id
                break
            if invoice!="":
                wizard.amount_late_fee_exclusive=wizard.amount
                wizard.late_fee=invoice.get_late_fee_charges(payment_date=wizard.payment_date)
                

    def _compute_amount(self):
        super(extwiz,self)._compute_amount()
        self._compute_late_fee()
        for wizard in self:
            wizard.amount=wizard.amount+wizard.late_fee
            
    def _create_payments(self):
        late_fee=self.late_fee
        amount_late_fee_exclusive=self.amount_late_fee_exclusive
        payments=super(extwiz,self)._create_payments()
        for payment in payments:
            payment.late_fee=late_fee
            payment.amount_late_fee_exclusive=payment.amount - payment.late_fee
        return payments
    
    def action_create_payments(self):
        for wizard in self:
            invoice=""
            for line in wizard.line_ids:
                invoice=line.move_id
                break
            if invoice!="":
                invoice.apply_late_fee_policy(payment_date=wizard.payment_date)
                invoice.assert_balanced() 
                invoice.exclude_from_invoice_tab = False 
        return super(extwiz,self).action_create_payments()


class ext_journal(models.Model):
    _inherit = "account.journal"
    apply_late_fee_policy = fields.Boolean(string='Apply Late Fee Policy',default=False)
    
class ext_invoice(models.Model):
    _inherit = "account.move"
    late_fee_compute = fields.Float(compute='_compute_late_fee_compute', string='late_fee_compute')
    
    @api.depends('invoice_date_due')
    def _compute_late_fee_compute(self):
        if self.payment_state=="paid" or self.state!="posted":
            self.late_fee_compute=0
        else:  
            self.late_fee_compute=self.get_late_fee_charges()
            
    def get_late_fee_charges(self,payment_date=None):
        
        
        invoice=self
        if invoice.journal_id==False:
            return 0    ## if no journal_id found, can't be sure if we should apply late fee or not. 
        if not invoice.journal_id.apply_late_fee_policy:
            return 0    ## if invoice is for admission challan, no late fee will be charged
        ##get todays date
        if payment_date:
            nowdate=payment_date
        else:
            nowdate=datetime.datetime.now().date()
        if nowdate<invoice.invoice_date_due:
            return 0    ##if due date has not exceeded, then latefee charges are zero. 
        ## get late fee slabs
        slabs=self.env["account.latefeeslab"].search([])
        ## sort slabs according to days
        policy=[]
        for slab in slabs:
            policy.append((slab.days,slab.charge))
        policy=sorted(policy,key=lambda x: x[0])
        ##creating dictionary for slabs for easier handling
        policydict={}
        for e in policy:
            policydict[e[0]]=e[1]
        policy=policydict
        ##get total number of late days till now.
        Total_Late_Days=(nowdate-invoice.invoice_date_due).days
        ##calculate how much days each slab in policy gets. 
        remaining_days=Total_Late_Days 
        days={}
        previous_slab_days=0
        for current_slab_days in policy.keys():

            dif = current_slab_days - previous_slab_days 
            if dif>remaining_days:
                days[current_slab_days]=remaining_days
                remaining_days=0
                break
            days[current_slab_days] = dif
            remaining_days = remaining_days - dif
            charge=policy[current_slab_days]
            previous_slab_days=current_slab_days
        if remaining_days>0:
            days["remaining"]=remaining_days
            policy["remaining"]=charge
        
        ##calculate total charges for each slab.
        charges={}                   
        for key in days.keys():
            charge=policy[key]
            numberOfdays=days[key]
            if key is "remaining":##If number of days are going beyond the defined slab, then add the given amount every 10 days. 
#                 raise UserError(str(numberOfdays)+" : "+str(dif)+" : "+str(int(numberOfdays/dif))+" : "+str(charge*(2+int(numberOfdays/dif)))))
                charges[key]=charge*(2+int(numberOfdays/dif))
            else:
                charges[key]=charge ## add the defined amount for this slab only. 
        
        # ## sum all charges
        # sum_of_all_charges=0
        # for key in days.keys():
        #     sum_of_all_charges+=charges[key]
        # return sum_of_all_charges

        ##max of all charges
        max=0
        for key in days.keys():
            if charges[key]>max:
                max=charges[key]
        return max        
    # @api.onchange('state')
    def apply_late_fee_policy(self,payment_date=None):
        #raise UserError(self._compute_amount())

        
        for invoice in self:
            late_fee_charges=invoice.get_late_fee_charges(payment_date=payment_date)
            # raise UserError(late_fee_charges)
        
            #late_fee_charges=invoice._compute_late_fee()
            
            if late_fee_charges<=0:
                return
            ##late fee calculations are complete. now to put these charges in to the invoice lines.
            ##reset invoice to draft to be able to insert the new line
            invoice.button_draft()
            # raise UserError(late_fee_charges)
            ##find any pre existing line for late fee. 

            foundline=None
            for line in invoice.invoice_line_ids:
                if line.product_id.name=="Late Fee":
                    
                    foundline=line
                    break
            ##if line is found. adding all charges to it.
            if foundline is not None:
                #--------------------------------------#
                
                foundline.price_unit=late_fee_charges
            else:   ##else creating new late fee line and adding charges there
                latefee_product=self.env["product.product"].search([("name","=","Late Fee")])
                latefee_account=self.env["account.account"].search([("name","=","Late Fee")])
                if len(latefee_product)<1:
                    raise UserError("Late Fee charges item not found. Cannot proceed further. Make sure you have added the Late Fee charge.")  ## cannot continue if the late fee product hasn't been added. 
                if len(latefee_account)<1:
                    raise UserError("Late Fee account not found. Cannot proceed further. Make sure you have added the late fee account in accounts.")## cannot continue if the late fee account hasn't been added. 
                latefee_product=latefee_product[0]
                latefee_account=latefee_account[0]
                data={
                    "product_id":latefee_product.id,
                    "account_id":latefee_account.id,
                    "name":latefee_product.name,
                    "price_unit":late_fee_charges
                }
                invoice.invoice_line_ids=[(0,0,data)]
            invoice.action_post()


            

            
