
from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
import json





class ext(models.Model):
    _inherit="account.move"

    month_date=fields.Char(string="Month",compute="_get_month_date")
    year_date=fields.Char(string="Year",compute="_get_year_date")
#     month_total=fields.Char(string="Month Total",compute="_get_month_date")
    
    def refund_receive_action(self):
        if not self.x_studio_receiverefund:
            self.x_studio_receiverefund=self.refund_receive
    
    def _get_month_date(self):
        self.month_date=''
        for rec in self:
            due_date=str(rec.invoice_date)
            splitted_name=due_date.split('-')
            if len(splitted_name)>2:
                month_in_number=splitted_name[1]
                if month_in_number == '12':
                    rec['month_date']='December'
                elif month_in_number == '11':
                    rec['month_date']='November'
                elif month_in_number == '10':
                    rec['month_date']='October'
                elif month_in_number == '09':
                    rec['month_date']='September'
                elif month_in_number == '08':
                    rec['month_date']='August'
                elif month_in_number == '07':
                    rec['month_date']='July'
                elif month_in_number == '06':
                    rec['month_date']='June'
                elif month_in_number == '05':
                    rec['month_date']='May'
                elif month_in_number == '04':
                    rec['month_date']='April'
                elif month_in_number == '03':
                    rec['month_date']='March'
                elif month_in_number == '02':
                    rec['month_date']='Feburary'
                elif month_in_number == '01':
                    rec['month_date']='January'

    def _get_year_date(self):
        self.year_date=''
        for rec in self:
            due_date=str(rec.invoice_date)
            splitted_name=due_date.split('-')
            if len(splitted_name)>2:
                year_in_number=splitted_name[0]
                rec['year_date']=year_in_number[2:4]

                
                
    
    # def _get_monthly_total(self):
    #     for rec in self:

    #         if rec.move_type=="out_refund":

                    
                        
        


                

                       
        
        



#     # security_price=fields.Integer(string='Security Price')
   
#     tuition=fields.Integer(string="Tuition Fee", compute='_onchange_tuition')
#     club=fields.Integer(string="Club Charges", compute="_onchange_club")
#     computer=fields.Integer(string="computer Charges", compute="_onchange_computer")
#     library=fields.Integer(string="library Charges", compute="_onchange_library")
#     utility=fields.Integer(string="utility Charges", compute="_onchange_utility")
#     stud
