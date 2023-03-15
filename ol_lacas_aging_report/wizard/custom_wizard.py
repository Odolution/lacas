
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
import xlsxwriter
_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


import base64

import io
try:
    import xlwt
except ImportError:
    xlwt = None

class GroupAging(models.Model):
    _name = 'aging.invoice.group'

    name  =  fields.Char(string="Name")
    grouping = fields.Char('Groups')

class AccountMoveReport(models.TransientModel):
    _name = 'account.aging.move.line'
    


    student_branch=fields.Char('Branch')
    student_campus=fields.Char('Campus')


    #-------------------------------------------------------------2022-------------------------------------------------------

    recievable_jan=fields.Integer('JAN-22')
    ondue_jan=fields.Integer('JAN-22')
    afterdue_jan=fields.Integer('JAN-22')
    firstmon_jan=fields.Integer('JAN-22')
    secmon_jan=fields.Integer('JAN-22')
    thirdmon_jan=fields.Integer('JAN-22')
    actual_recievable_jan=fields.Integer('JAN-22')
    total_recieve_jan=fields.Integer('JAN-22')
    bad_debt_jan=fields.Integer('JAN-22')
    percentage_bd_jan=fields.Integer('JAN-22')


  
    recievable_feb=fields.Integer('FEB-22')
    ondue_feb=fields.Integer('FEB-22')
    afterdue_feb=fields.Integer('FEB-22')
    firstmon_feb=fields.Integer('FEB-22')
    secmon_feb=fields.Integer('FEB-22')
    thirdmon_feb=fields.Integer('FEB-22')
    actual_recievable_feb=fields.Integer('FEB-22')
    total_recieve_feb=fields.Integer('FEB-22')
    bad_debt_feb=fields.Integer('FEB-22')
    percentage_bd_feb=fields.Integer('FEB-22')


    recievable_mar=fields.Integer('MAR-22')
    ondue_mar=fields.Integer('MAR-22')
    afterdue_mar=fields.Integer('MAR-22')
    firstmon_mar=fields.Integer('MAR-22')
    secmon_mar=fields.Integer('MAR-22')
    thirdmon_mar=fields.Integer('MAR-22')
    actual_recievable_mar=fields.Integer('MAR-22')
    total_recieve_mar=fields.Integer('MAR-22')
    bad_debt_mar=fields.Integer('MAR-22')
    percentage_bd_mar=fields.Integer('MAR-22')

    recievable_apr=fields.Integer('APR-22')
    ondue_apr=fields.Integer('APR-22')
    afterdue_apr=fields.Integer('APR-22')
    firstmon_apr=fields.Integer('APR-22')
    secmon_apr=fields.Integer('APR-22')
    thirdmon_apr=fields.Integer('APR-22')
    actual_recievable_apr=fields.Integer('APR-22')
    total_recieve_apr=fields.Integer('APR-22')
    bad_debt_apr=fields.Integer('APR-22')
    percentage_bd_apr=fields.Integer('APR-22')

    recievable_may=fields.Integer('MAY-22')
    ondue_may=fields.Integer('MAY-22')
    afterdue_may=fields.Integer('MAY-22')
    firstmon_may=fields.Integer('MAY-22')
    secmon_may=fields.Integer('MAY-22')
    thirdmon_may=fields.Integer('MAY-22')
    actual_recievable_may=fields.Integer('MAY-22')
    total_recieve_may=fields.Integer('MAY-22')
    bad_debt_may=fields.Integer('MAY-22')
    percentage_bd_may=fields.Integer('MAY-22')

    recievable_jun=fields.Integer('JUN-22')
    ondue_jun=fields.Integer('JUN-22')
    afterdue_jun=fields.Integer('JUN-22')
    firstmon_jun=fields.Integer('JUN-22')
    secmon_jun=fields.Integer('JUN-22')
    thirdmon_jun=fields.Integer('JUN-22')
    actual_recievable_jun=fields.Integer('JUN-22')
    total_recieve_jun=fields.Integer('JUN-22')
    bad_debt_jun=fields.Integer('JUN-22')
    percentage_bd_jun=fields.Integer('JUN-22')

    recievable_jul=fields.Integer('JUL-22')
    ondue_jul=fields.Integer('JUL-22')
    afterdue_jul=fields.Integer('JUL-22')
    firstmon_jul=fields.Integer('JUL-22')
    secmon_jul=fields.Integer('JUL-22')
    thirdmon_jul=fields.Integer('JUL-22')
    actual_recievable_jul=fields.Integer('JUL-22')
    total_recieve_jul=fields.Integer('JUL-22')
    bad_debt_jul=fields.Integer('JUL-22')
    percentage_bd_jul=fields.Integer('JUL-22')

    recievable_aug=fields.Integer('AUG-22')
    ondue_aug=fields.Integer('AUG-22')
    afterdue_aug=fields.Integer('AUG-22')
    firstmon_aug=fields.Integer('AUG-22')
    secmon_aug=fields.Integer('AUG-22')
    thirdmon_aug=fields.Integer('AUG-22')
    actual_recievable_aug=fields.Integer('AUG-22')
    total_recieve_aug=fields.Integer('AUG-22')
    bad_debt_aug=fields.Integer('AUG-22')
    percentage_bd_aug=fields.Integer('AUG-22')

    recievable_sep=fields.Integer('SEP-22')
    ondue_sep=fields.Integer('SEP-22')
    afterdue_sep=fields.Integer('SEP-22')
    firstmon_sep=fields.Integer('SEP-22')
    secmon_sep=fields.Integer('SEP-22')
    thirdmon_sep=fields.Integer('SEP-22')
    actual_recievable_sep=fields.Integer('SEP-22')
    total_recieve_sep=fields.Integer('SEP-22')
    bad_debt_sep=fields.Integer('SEP-22')
    percentage_bd_sep=fields.Integer('SEP-22')

    recievable_oct=fields.Integer('OCT-22')
    ondue_oct=fields.Integer('OCT-22')
    afterdue_oct=fields.Integer('OCT-22')
    firstmon_oct=fields.Integer('OCT-22')
    secmon_oct=fields.Integer('OCT-22')
    thirdmon_oct=fields.Integer('OCT-22')
    actual_recievable_oct=fields.Integer('OCT-22')
    total_recieve_oct=fields.Integer('OCT-22')
    bad_debt_oct=fields.Integer('OCT-22')
    percentage_bd_oct=fields.Integer('OCT-22')

    recievable_nov=fields.Integer('NOV-22')
    ondue_nov=fields.Integer('NOV-22')
    afterdue_nov=fields.Integer('NOV-22')
    firstmon_nov=fields.Integer('NOV-22')
    secmon_nov=fields.Integer('NOV-22')
    thirdmon_nov=fields.Integer('NOV-22')
    actual_recievable_nov=fields.Integer('NOV-22')
    total_recieve_nov=fields.Integer('NOV-22')
    bad_debt_nov=fields.Integer('NOV-22')
    percentage_bd_nov=fields.Integer('NOV-22')

    recievable_dec=fields.Integer('DEC-22')
    ondue_dec=fields.Integer('DEC-22')
    afterdue_dec=fields.Integer('DEC-22')
    firstmon_dec=fields.Integer('DEC-22')
    secmon_dec=fields.Integer('DEC-22')
    thirdmon_dec=fields.Integer('DEC-22')
    actual_recievable_dec=fields.Integer('DEC-22')
    total_recieve_dec=fields.Integer('DEC-22')
    bad_debt_dec=fields.Integer('DEC-22')
    percentage_bd_dec=fields.Integer('DEC-22')

#-------------------------------------------------------------2023-------------------------------------------------------



    recievable_jan_2=fields.Integer('JAN-23')
    ondue_jan_2=fields.Integer('JAN-23')
    afterdue_jan_2=fields.Integer('JAN-23')
    firstmon_jan_2=fields.Integer('JAN-23')
    secmon_jan_2=fields.Integer('JAN-23')
    thirdmon_jan_2=fields.Integer('JAN-23')
    actual_recievable_jan_2=fields.Integer('JAN-23')
    total_recieve_jan_2=fields.Integer('JAN-23')
    bad_debt_jan_2=fields.Integer('JAN-23')
    percentage_bd_jan_2=fields.Integer('JAN-23')


  
    recievable_feb_2=fields.Integer('FEB-23')
    ondue_feb_2=fields.Integer('FEB-23')
    afterdue_feb_2=fields.Integer('FEB-23')
    firstmon_feb_2=fields.Integer('FEB-23')
    secmon_feb_2=fields.Integer('FEB-23')
    thirdmon_feb_2=fields.Integer('FEB-23')
    actual_recievable_feb_2=fields.Integer('FEB-23')
    total_recieve_feb_2=fields.Integer('FEB-23')
    bad_debt_feb_2=fields.Integer('FEB-23')
    percentage_bd_feb_2=fields.Integer('FEB-23')


    recievable_mar_2=fields.Integer('MAR-23')
    ondue_mar_2=fields.Integer('MAR-23')
    afterdue_mar_2=fields.Integer('MAR-23')
    firstmon_mar_2=fields.Integer('MAR-23')
    secmon_mar_2=fields.Integer('MAR-23')
    thirdmon_mar_2=fields.Integer('MAR-23')
    actual_recievable_mar_2=fields.Integer('MAR-23')
    total_recieve_mar_2=fields.Integer('MAR-23')
    bad_debt_mar_2=fields.Integer('MAR-23')
    percentage_bd_mar_2=fields.Integer('MAR-23')

    recievable_apr_2=fields.Integer('APR-23')
    ondue_apr_2=fields.Integer('APR-23')
    afterdue_apr_2=fields.Integer('APR-23')
    firstmon_apr_2=fields.Integer('APR-23')
    secmon_apr_2=fields.Integer('APR-23')
    thirdmon_apr_2=fields.Integer('APR-23')
    actual_recievable_apr_2=fields.Integer('APR-23')
    total_recieve_apr_2=fields.Integer('APR-23')
    bad_debt_apr_2=fields.Integer('APR-23')
    percentage_bd_apr_2=fields.Integer('APR-23')

    recievable_may_2=fields.Integer('MAY-23')
    ondue_may_2=fields.Integer('MAY-23')
    afterdue_may_2=fields.Integer('MAY-23')
    firstmon_may_2=fields.Integer('MAY-23')
    secmon_may_2=fields.Integer('MAY-23')
    thirdmon_may_2=fields.Integer('MAY-23')
    actual_recievable_may_2=fields.Integer('MAY-23')
    total_recieve_may_2=fields.Integer('MAY-23')
    bad_debt_may_2=fields.Integer('MAY-23')
    percentage_bd_may_2=fields.Integer('MAY-23')

    recievable_jun_2=fields.Integer('JUN-23')
    ondue_jun_2=fields.Integer('JUN-23')
    afterdue_jun_2=fields.Integer('JUN-23')
    firstmon_jun_2=fields.Integer('JUN-23')
    secmon_jun_2=fields.Integer('JUN-23')
    thirdmon_jun_2=fields.Integer('JUN-23')
    actual_recievable_jun_2=fields.Integer('JUN-23')
    total_recieve_jun_2=fields.Integer('JUN-23')
    bad_debt_jun_2=fields.Integer('JUN-23')
    percentage_bd_jun_2=fields.Integer('JUN-23')

    recievable_jul_2=fields.Integer('JUL-23')
    ondue_jul_2=fields.Integer('JUL-23')
    afterdue_jul_2=fields.Integer('JUL-23')
    firstmon_jul_2=fields.Integer('JUL-23')
    secmon_jul_2=fields.Integer('JUL-23')
    thirdmon_jul_2=fields.Integer('JUL-23')
    actual_recievable_jul_2=fields.Integer('JUL-23')
    total_recieve_jul_2=fields.Integer('JUL-23')
    bad_debt_jul_2=fields.Integer('JUL-23')
    percentage_bd_jul_2=fields.Integer('JUL-23')

    recievable_aug_2=fields.Integer('AUG-23')
    ondue_aug_2=fields.Integer('AUG-23')
    afterdue_aug_2=fields.Integer('AUG-23')
    firstmon_aug_2=fields.Integer('AUG-23')
    secmon_aug_2=fields.Integer('AUG-23')
    thirdmon_aug_2=fields.Integer('AUG-23')
    actual_recievable_aug_2=fields.Integer('AUG-23')
    total_recieve_aug_2=fields.Integer('AUG-23')
    bad_debt_aug_2=fields.Integer('AUG-23')
    percentage_bd_aug_2=fields.Integer('AUG-23')

    recievable_sep_2=fields.Integer('SEP-23')
    ondue_sep_2=fields.Integer('SEP-23')
    afterdue_sep_2=fields.Integer('SEP-23')
    firstmon_sep_2=fields.Integer('SEP-23')
    secmon_sep_2=fields.Integer('SEP-23')
    thirdmon_sep_2=fields.Integer('SEP-23')
    actual_recievable_sep_2=fields.Integer('SEP-23')
    total_recieve_sep_2=fields.Integer('SEP-23')
    bad_debt_sep_2=fields.Integer('SEP-23')
    percentage_bd_sep_2=fields.Integer('SEP-23')

    recievable_oct_2=fields.Integer('OCT-23')
    ondue_oct_2=fields.Integer('OCT-23')
    afterdue_oct_2=fields.Integer('OCT-23')
    firstmon_oct_2=fields.Integer('OCT-23')
    secmon_oct_2=fields.Integer('OCT-23')
    thirdmon_oct_2=fields.Integer('OCT-23')
    actual_recievable_oct_2=fields.Integer('OCT-23')
    total_recieve_oct_2=fields.Integer('OCT-23')
    bad_debt_oct_2=fields.Integer('OCT-23')
    percentage_bd_oct_2=fields.Integer('OCT-23')

    recievable_nov_2=fields.Integer('NOV-23')
    ondue_nov_2=fields.Integer('NOV-23')
    afterdue_nov_2=fields.Integer('NOV-23')
    firstmon_nov_2=fields.Integer('NOV-23')
    secmon_nov_2=fields.Integer('NOV-23')
    thirdmon_nov_2=fields.Integer('NOV-23')
    actual_recievable_nov_2=fields.Integer('NOV-23')
    total_recieve_nov_2=fields.Integer('NOV-23')
    bad_debt_nov_2=fields.Integer('NOV-23')
    percentage_bd_nov_2=fields.Integer('NOV-23')

    recievable_dec_2=fields.Integer('DEC-23')
    ondue_dec_2=fields.Integer('DEC-23')
    afterdue_dec_2=fields.Integer('DEC-23')
    firstmon_dec_2=fields.Integer('DEC-23')
    secmon_dec_2=fields.Integer('DEC-23')
    thirdmon_dec_2=fields.Integer('DEC-23')
    actual_recievable_dec_2=fields.Integer('DEC-23')
    total_recieve_dec_2=fields.Integer('DEC-23')
    bad_debt_dec_2=fields.Integer('DEC-23')
    percentage_bd_dec_2=fields.Integer('DEC-23')


    
   

class agingsReportWizard(models.TransientModel):
    _name="aging.report.wizard"
    _description='Print aging Wizard'

    date_from=fields.Date(string="Date From")
    date_to=fields.Date(string="Date To")

    account_report_line=fields.Many2many('account.aging.move.line', string='Account report Line')
    groups_ids = fields.Many2many('aging.invoice.group', string='Groups')


  
    
    def action_print_report(self):

        

        move_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('payment_state','in',['not_paid','paid']),("invoice_date",">=",self.date_from),("invoice_date","<=",self.date_to)])
        branch_lst=[]

        for inv in move_ids:
            if len(inv.program_ids)==1:
                if inv.program_ids not in branch_lst:
                    branch_lst.append(inv.program_ids)

        lines=[]
        for branch in branch_lst:

           
            branch_wise_inv=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('journal_id','=',125),('payment_state','in',['not_paid','paid']),("invoice_date",">=",self.date_from),("invoice_date","<=",self.date_to)])
          
            for value in branch_wise_inv:
                if value.program_ids==branch:

                    custom_data = {
                   
                        "student_branch":"",
                        "student_campus":'',

                        #------jan22-------
                       
                        "recievable_jan": 0,
                        "ondue_jan": 0,
                        "afterdue_jan": 0,
                        "firstmon_jan":0,
                        "secmon_jan":0,
                        "thirdmon_jan": 0,
                        "actual_recievable_jan":0,
                        "total_recieve_jan":0,
                        "bad_debt_jan": 0,
                        "percentage_bd_jan": 0,

                        
                        #------feb22-------
                       
                        "recievable_feb": 0,
                        "ondue_feb": 0,
                        "afterdue_feb": 0,
                        "firstmon_feb":0,
                        "secmon_feb":0,
                        "thirdmon_feb": 0,
                        "actual_recievable_feb":0,
                        "total_recieve_feb":0,
                        "bad_debt_feb": 0,
                        "percentage_bd_feb": 0,

                        
                        #------mar22-------
                       
                        "recievable_mar": 0,
                        "ondue_mar": 0,
                        "afterdue_mar": 0,
                        "firstmon_mar":0,
                        "secmon_mar":0,
                        "thirdmon_mar": 0,
                        "actual_recievable_mar":0,
                        "total_recieve_mar":0,
                        "bad_debt_mar": 0,
                        "percentage_bd_mar": 0,

                        
                        #------apr22-------
                       
                        "recievable_apr": 0,
                        "ondue_apr": 0,
                        "afterdue_apr": 0,
                        "firstmon_apr":0,
                        "secmon_apr":0,
                        "thirdmon_apr": 0,
                        "actual_recievable_apr":0,
                        "total_recieve_apr":0,
                        "bad_debt_apr": 0,
                        "percentage_bd_apr": 0,

                        
                        #------may22-------
                       
                        "recievable_may": 0,
                        "ondue_may": 0,
                        "afterdue_may": 0,
                        "firstmon_may":0,
                        "secmon_may":0,
                        "thirdmon_may": 0,
                        "actual_recievable_may":0,
                        "total_recieve_may":0,
                        "bad_debt_may": 0,
                        "percentage_bd_may": 0,

                        
                        #------jun22-------
                       
                        "recievable_jun": 0,
                        "ondue_jun": 0,
                        "afterdue_jun": 0,
                        "firstmon_jun":0,
                        "secmon_jun":0,
                        "thirdmon_jun": 0,
                        "actual_recievable_jun":0,
                        "total_recieve_jun":0,
                        "bad_debt_jun": 0,
                        "percentage_bd_jun": 0,

                        
                        #------jul22-------
                       
                        "recievable_jul": 0,
                        "ondue_jul": 0,
                        "afterdue_jul": 0,
                        "firstmon_jul":0,
                        "secmon_jul":0,
                        "thirdmon_jul": 0,
                        "actual_recievable_jul":0,
                        "total_recieve_jul":0,
                        "bad_debt_jul": 0,
                        "percentage_bd_jul": 0,

                        
                        #------aug22-------
                       
                        "recievable_aug": 0,
                        "ondue_aug": 0,
                        "afterdue_aug": 0,
                        "firstmon_aug":0,
                        "secmon_aug":0,
                        "thirdmon_aug": 0,
                        "actual_recievable_aug":0,
                        "total_recieve_aug":0,
                        "bad_debt_aug": 0,
                        "percentage_bd_aug": 0,

                        
                        #------sep22-------
                       
                        "recievable_sep": 0,
                        "ondue_sep": 0,
                        "afterdue_sep": 0,
                        "firstmon_sep":0,
                        "secmon_sep":0,
                        "thirdmon_sep": 0,
                        "actual_recievable_sep":0,
                        "total_recieve_sep":0,
                        "bad_debt_sep": 0,
                        "percentage_bd_sep": 0,

                        
                        #------oct22-------
                       
                        "recievable_oct": 0,
                        "ondue_oct": 0,
                        "afterdue_oct": 0,
                        "firstmon_oct":0,
                        "secmon_oct":0,
                        "thirdmon_oct": 0,
                        "actual_recievable_oct":0,
                        "total_recieve_oct":0,
                        "bad_debt_oct": 0,
                        "percentage_bd_oct": 0,

                        
                        #------nov22-------
                       
                        "recievable_nov": 0,
                        "ondue_nov": 0,
                        "afterdue_nov": 0,
                        "firstmon_nov":0,
                        "secmon_nov":0,
                        "thirdmon_nov": 0,
                        "actual_recievable_nov":0,
                        "total_recieve_nov":0,
                        "bad_debt_nov": 0,
                        "percentage_bd_nov": 0,

                        
                        #------dec22-------
                       
                        "recievable_dec": 0,
                        "ondue_dec": 0,
                        "afterdue_dec": 0,
                        "firstmon_dec":0,
                        "secmon_dec":0,
                        "thirdmon_dec": 0,
                        "actual_recievable_dec":0,
                        "total_recieve_dec":0,
                        "bad_debt_dec": 0,
                        "percentage_bd_dec": 0,

                             #------jan23-------
                       
                        "recievable_jan_2": 0,
                        "ondue_jan_2": 0,
                        "afterdue_jan_2": 0,
                        "firstmon_jan_2":0,
                        "secmon_jan_2":0,
                        "thirdmon_jan_2": 0,
                        "actual_recievable_jan_2":0,
                        "total_recieve_jan_2":0,
                        "bad_debt_jan_2": 0,
                        "percentage_bd_jan_2": 0,

                        
                        #------feb23-------
                       
                        "recievable_feb_2": 0,
                        "ondue_feb_2": 0,
                        "afterdue_feb_2": 0,
                        "firstmon_feb_2":0,
                        "secmon_feb_2":0,
                        "thirdmon_feb_2": 0,
                        "actual_recievable_feb_2":0,
                        "total_recieve_feb_2":0,
                        "bad_debt_feb_2": 0,
                        "percentage_bd_feb_2": 0,

                        
                        #------mar23-------
                       
                        "recievable_mar_2": 0,
                        "ondue_mar_2": 0,
                        "afterdue_mar_2": 0,
                        "firstmon_mar_2":0,
                        "secmon_mar_2":0,
                        "thirdmon_mar_2": 0,
                        "actual_recievable_mar_2":0,
                        "total_recieve_mar_2":0,
                        "bad_debt_mar_2": 0,
                        "percentage_bd_mar_2": 0,

                        
                        #------apr23-------
                       
                        "recievable_apr_2": 0,
                        "ondue_apr_2": 0,
                        "afterdue_apr_2": 0,
                        "firstmon_apr_2":0,
                        "secmon_apr_2":0,
                        "thirdmon_apr_2": 0,
                        "actual_recievable_apr_2":0,
                        "total_recieve_apr_2":0,
                        "bad_debt_apr_2": 0,
                        "percentage_bd_apr_2": 0,

                        
                        #------may23-------
                       
                        "recievable_may_2": 0,
                        "ondue_may_2": 0,
                        "afterdue_may_2": 0,
                        "firstmon_may_2":0,
                        "secmon_may_2":0,
                        "thirdmon_may_2": 0,
                        "actual_recievable_may_2":0,
                        "total_recieve_may_2":0,
                        "bad_debt_may_2": 0,
                        "percentage_bd_may_2": 0,

                        
                        #------jun23-------
                       
                        "recievable_jun_2": 0,
                        "ondue_jun_2": 0,
                        "afterdue_jun_2": 0,
                        "firstmon_jun_2":0,
                        "secmon_jun_2":0,
                        "thirdmon_jun_2": 0,
                        "actual_recievable_jun_2":0,
                        "total_recieve_jun_2":0,
                        "bad_debt_jun_2": 0,
                        "percentage_bd_jun_2": 0,

                        
                        #------jul23-------
                       
                        "recievable_jul_2": 0,
                        "ondue_jul_2": 0,
                        "afterdue_jul_2": 0,
                        "firstmon_jul_2":0,
                        "secmon_jul_2":0,
                        "thirdmon_jul_2": 0,
                        "actual_recievable_jul_2":0,
                        "total_recieve_jul_2":0,
                        "bad_debt_jul_2": 0,
                        "percentage_bd_jul_2": 0,

                        
                        #------aug23-------
                       
                        "recievable_aug_2": 0,
                        "ondue_aug_2": 0,
                        "afterdue_aug_2": 0,
                        "firstmon_aug_2":0,
                        "secmon_aug_2":0,
                        "thirdmon_aug_2": 0,
                        "actual_recievable_aug_2":0,
                        "total_recieve_aug_2":0,
                        "bad_debt_aug_2": 0,
                        "percentage_bd_aug_2": 0,

                        
                        #------sep23-------
                       
                        "recievable_sep_2": 0,
                        "ondue_sep_2": 0,
                        "afterdue_sep_2": 0,
                        "firstmon_sep_2":0,
                        "secmon_sep_2":0,
                        "thirdmon_sep_2": 0,
                        "actual_recievable_sep_2":0,
                        "total_recieve_sep_2":0,
                        "bad_debt_sep_2": 0,
                        "percentage_bd_sep_2": 0,

                        
                        #------oct23-------
                       
                        "recievable_oct_2": 0,
                        "ondue_oct_2": 0,
                        "afterdue_oct_2": 0,
                        "firstmon_oct_2":0,
                        "secmon_oct_2":0,
                        "thirdmon_oct_2": 0,
                        "actual_recievable_oct_2":0,
                        "total_recieve_oct_2":0,
                        "bad_debt_oct_2": 0,
                        "percentage_bd_oct_2": 0,

                        
                        #------nov23-------
                       
                        "recievable_nov_2": 0,
                        "ondue_nov_2": 0,
                        "afterdue_nov_2": 0,
                        "firstmon_nov_2":0,
                        "secmon_nov_2":0,
                        "thirdmon_nov_2": 0,
                        "actual_recievable_nov_2":0,
                        "total_recieve_nov_2":0,
                        "bad_debt_nov_2": 0,
                        "percentage_bd_nov_2": 0,

                        
                        #------dec23-------
                       
                        "recievable_dec_2": 0,
                        "ondue_dec_2": 0,
                        "afterdue_dec_2": 0,
                        "firstmon_dec_2":0,
                        "secmon_dec_2":0,
                        "thirdmon_dec_2": 0,
                        "actual_recievable_dec_2":0,
                        "total_recieve_dec_2":0,
                        "bad_debt_dec_2": 0,
                        "percentage_bd_dec_2": 0,

                    } 

                    custom_data['student_branch'] = value.program_ids if  len(value.program_ids)==1  else ""
                    custom_data['student_campus'] = value.campus if value.campus else ''

                    if value.month_date == "January" and value.year_date=='22':
                        custom_data['recievable_jan'] += value.amount_residual
                        custom_data['recievable_jan'] += (int(value.bill_amount))

                    elif value.month_date == "Feburary" and value.year_date=='22':
                        custom_data['recievable_feb'] += value.amount_residual
                        custom_data['recievable_feb'] += int(value.bill_amount)

                    elif value.month_date == "March"and value.year_date=='22':
                        custom_data['recievable_mar'] += value.amount_residual
                        custom_data['recievable_mar'] += int(value.bill_amount)

                    elif value.month_date == "April" and value.year_date=='22':
                        custom_data['recievable_apr'] += value.amount_residual
                        custom_data['recievable_apr'] += int(value.bill_amount)


                    elif value.month_date == "May" and value.year_date=='22':
                        custom_data['recievable_may'] += value.amount_residual
                        custom_data['recievable_may'] += int(value.bill_amount)


                    elif value.month_date == "June" and value.year_date=='22':
                        custom_data['recievable_jun'] += value.amount_residual
                        custom_data['recievable_jun'] += int(value.bill_amount)


                    elif value.month_date == "July" and value.year_date=='22':
                        custom_data['recievable_jul'] += value.amount_residual
                        custom_data['recievable_jul'] += int(value.bill_amount)

                    elif value.month_date == "August" and value.year_date=='22':
                        custom_data['recievable_aug'] += value.amount_residual
                        custom_data['recievable_aug'] += int(value.bill_amount)

                    elif value.month_date == "September" and value.year_date=='22':
                        custom_data['recievable_sep'] += value.amount_residual
                        custom_data['recievable_sep'] += int(value.bill_amount)

                    elif value.month_date == "October" and value.year_date=='22':
                        custom_data['recievable_oct'] += value.amount_residual
                        custom_data['recievable_oct'] += int(value.bill_amount)

                    elif value.month_date == "November" and value.year_date=='22':
                        custom_data['recievable_nov'] += value.amount_residual
                        custom_data['recievable_nov'] += int(value.bill_amount)

                    elif value.month_date == "December" and value.year_date=='22':
                        custom_data['recievable_dec'] += value.amount_residual
                        custom_data['recievable_dec'] += int(value.bill_amount)

                    elif value.month_date == "January" and value.year_date=='23':
                        custom_data['recievable_jan_2'] += value.amount_residual
                        custom_data['recievable_jan_2'] += int(value.bill_amount)

                    elif value.month_date == "Feburary" and value.year_date=='23':
                        custom_data['recievable_feb_2'] += value.amount_residual
                        custom_data['recievable_feb_2'] += int(value.bill_amount)

                    elif value.month_date == "March"and value.year_date=='23':
                        custom_data['recievable_mar_2'] += value.amount_residual
                        custom_data['recievable_mar_2'] += int(value.bill_amount)

                    elif value.month_date == "April" and value.year_date=='23':
                        custom_data['recievable_apr_2'] += value.amount_residual
                        custom_data['recievable_apr_2'] += int(value.bill_amount)

                    elif value.month_date == "May" and value.year_date=='23':
                        custom_data['recievable_may_2'] += value.amount_residual
                        custom_data['recievable_may_2'] += int(value.bill_amount)

                    elif value.month_date == "June" and value.year_date=='23':
                        custom_data['recievable_jun_2'] += value.amount_residual
                        custom_data['recievable_jun_2'] += int(value.bill_amount)

                    elif value.month_date == "July" and value.year_date=='23':
                        custom_data['recievable_jul_2'] += value.amount_residual
                        custom_data['recievable_jul_2'] += int(value.bill_amount)

                    elif value.month_date == "August" and value.year_date=='23':
                        custom_data['recievable_aug_2'] += value.amount_residual
                        custom_data['recievable_aug_2'] += int(value.bill_amount)

                    elif value.month_date == "September" and value.year_date=='23':
                        custom_data['recievable_sep_2'] += value.amount_residual
                        custom_data['recievable_sep_2'] += int(value.bill_amount)

                    elif value.month_date == "October" and value.year_date=='23':
                        custom_data['recievable_oct_2'] += value.amount_residual
                        custom_data['recievable_oct_2'] += int(value.bill_amount)

                    elif value.month_date == "November" and value.year_date=='23':
                        custom_data['recievable_nov_2'] += value.amount_residual
                        custom_data['recievable_nov_2'] += int(value.bill_amount)

                    elif value.month_date == "December" and value.year_date=='23':
                        custom_data['recievable_dec_2'] += value.amount_residual
                        custom_data['recievable_dec_2'] += int(value.bill_amount)
            

            
        
                    mvl=self.env['account.aging.move.line'].create({
                        
                        "student_branch":custom_data['student_branch'],
                        "student_campus":custom_data['student_campus'],
                       #------jan22-------

                        "recievable_jan": custom_data['recievable_jan'],
                        "ondue_jan": 0,
                        "afterdue_jan": 0,
                        "firstmon_jan":0,
                        "secmon_jan":0,
                        "thirdmon_jan": 0,
                        "actual_recievable_jan":0,
                        "total_recieve_jan":0,
                        "bad_debt_jan": 0,
                        "percentage_bd_jan": 0,

                        
                        #------feb22-------
                       
                        "recievable_feb":  custom_data['recievable_feb'],
                        "ondue_feb": 0,
                        "afterdue_feb": 0,
                        "firstmon_feb":0,
                        "secmon_feb":0,
                        "thirdmon_feb": 0,
                        "actual_recievable_feb":0,
                        "total_recieve_feb":0,
                        "bad_debt_feb": 0,
                        "percentage_bd_feb": 0,

                        
                        #------mar22-------
                       
                        "recievable_mar":  custom_data['recievable_mar'],
                        "ondue_mar": 0,
                        "afterdue_mar": 0,
                        "firstmon_mar":0,
                        "secmon_mar":0,
                        "thirdmon_mar": 0,
                        "actual_recievable_mar":0,
                        "total_recieve_mar":0,
                        "bad_debt_mar": 0,
                        "percentage_bd_mar": 0,

                        
                        #------apr22-------
                       
                        "recievable_apr":  custom_data['recievable_apr'],
                        "ondue_apr": 0,
                        "afterdue_apr": 0,
                        "firstmon_apr":0,
                        "secmon_apr":0,
                        "thirdmon_apr": 0,
                        "actual_recievable_apr":0,
                        "total_recieve_apr":0,
                        "bad_debt_apr": 0,
                        "percentage_bd_apr": 0,

                        
                        #------may22-------
                       
                        "recievable_may":  custom_data['recievable_may'],
                        "ondue_may": 0,
                        "afterdue_may": 0,
                        "firstmon_may":0,
                        "secmon_may":0,
                        "thirdmon_may": 0,
                        "actual_recievable_may":0,
                        "total_recieve_may":0,
                        "bad_debt_may": 0,
                        "percentage_bd_may": 0,

                        
                        #------jun22-------
                       
                        "recievable_jun":  custom_data['recievable_jun'],
                        "ondue_jun": 0,
                        "afterdue_jun": 0,
                        "firstmon_jun":0,
                        "secmon_jun":0,
                        "thirdmon_jun": 0,
                        "actual_recievable_jun":0,
                        "total_recieve_jun":0,
                        "bad_debt_jun": 0,
                        "percentage_bd_jun": 0,

                        
                        #------jul22-------
                       
                        "recievable_jul":  custom_data['recievable_jul'],
                        "ondue_jul": 0,
                        "afterdue_jul": 0,
                        "firstmon_jul":0,
                        "secmon_jul":0,
                        "thirdmon_jul": 0,
                        "actual_recievable_jul":0,
                        "total_recieve_jul":0,
                        "bad_debt_jul": 0,
                        "percentage_bd_jul": 0,

                        
                        #------aug22-------
                       
                        "recievable_aug":  custom_data['recievable_aug'],
                        "ondue_aug": 0,
                        "afterdue_aug": 0,
                        "firstmon_aug":0,
                        "secmon_aug":0,
                        "thirdmon_aug": 0,
                        "actual_recievable_aug":0,
                        "total_recieve_aug":0,
                        "bad_debt_aug": 0,
                        "percentage_bd_aug": 0,

                        
                        #------sep22-------
                       
                        "recievable_sep":  custom_data['recievable_sep'],
                        "ondue_sep": 0,
                        "afterdue_sep": 0,
                        "firstmon_sep":0,
                        "secmon_sep":0,
                        "thirdmon_sep": 0,
                        "actual_recievable_sep":0,
                        "total_recieve_sep":0,
                        "bad_debt_sep": 0,
                        "percentage_bd_sep": 0,

                        
                        #------oct22-------
                       
                        "recievable_oct":  custom_data['recievable_oct'],
                        "ondue_oct": 0,
                        "afterdue_oct": 0,
                        "firstmon_oct":0,
                        "secmon_oct":0,
                        "thirdmon_oct": 0,
                        "actual_recievable_oct":0,
                        "total_recieve_oct":0,
                        "bad_debt_oct": 0,
                        "percentage_bd_oct": 0,

                        
                        #------nov22-------
                       
                        "recievable_nov":  custom_data['recievable_nov'],
                        "ondue_nov": 0,
                        "afterdue_nov": 0,
                        "firstmon_nov":0,
                        "secmon_nov":0,
                        "thirdmon_nov": 0,
                        "actual_recievable_nov":0,
                        "total_recieve_nov":0,
                        "bad_debt_nov": 0,
                        "percentage_bd_nov": 0,

                        
                        #------dec22-------
                       
                        "recievable_dec":  custom_data['recievable_dec'],
                        "ondue_dec": 0,
                        "afterdue_dec": 0,
                        "firstmon_dec":0,
                        "secmon_dec":0,
                        "thirdmon_dec": 0,
                        "actual_recievable_dec":0,
                        "total_recieve_dec":0,
                        "bad_debt_dec": 0,
                        "percentage_bd_dec": 0,

                             #------jan23-------
                       
                        "recievable_jan_2":  custom_data['recievable_jan_2'],
                        "ondue_jan_2": 0,
                        "afterdue_jan_2": 0,
                        "firstmon_jan_2":0,
                        "secmon_jan_2":0,
                        "thirdmon_jan_2": 0,
                        "actual_recievable_jan_2":0,
                        "total_recieve_jan_2":0,
                        "bad_debt_jan_2": 0,
                        "percentage_bd_jan_2": 0,

                        
                        #------feb23-------
                       
                        "recievable_feb_2":  custom_data['recievable_feb_2'],
                        "ondue_feb_2": 0,
                        "afterdue_feb_2": 0,
                        "firstmon_feb_2":0,
                        "secmon_feb_2":0,
                        "thirdmon_feb_2": 0,
                        "actual_recievable_feb_2":0,
                        "total_recieve_feb_2":0,
                        "bad_debt_feb_2": 0,
                        "percentage_bd_feb_2": 0,

                        
                        #------mar23-------
                       
                        "recievable_mar_2": custom_data['recievable_mar_2'],
                        "ondue_mar_2": 0,
                        "afterdue_mar_2": 0,
                        "firstmon_mar_2":0,
                        "secmon_mar_2":0,
                        "thirdmon_mar_2": 0,
                        "actual_recievable_mar_2":0,
                        "total_recieve_mar_2":0,
                        "bad_debt_mar_2": 0,
                        "percentage_bd_mar_2": 0,

                        
                        #------apr23-------
                       
                        "recievable_apr_2": custom_data['recievable_apr_2'],
                        "ondue_apr_2": 0,
                        "afterdue_apr_2": 0,
                        "firstmon_apr_2":0,
                        "secmon_apr_2":0,
                        "thirdmon_apr_2": 0,
                        "actual_recievable_apr_2":0,
                        "total_recieve_apr_2":0,
                        "bad_debt_apr_2": 0,
                        "percentage_bd_apr_2": 0,

                        
                        #------may23-------
                       
                        "recievable_may_2": custom_data['recievable_may_2'],
                        "ondue_may_2": 0,
                        "afterdue_may_2": 0,
                        "firstmon_may_2":0,
                        "secmon_may_2":0,
                        "thirdmon_may_2": 0,
                        "actual_recievable_may_2":0,
                        "total_recieve_may_2":0,
                        "bad_debt_may_2": 0,
                        "percentage_bd_may_2": 0,

                        
                        #------jun23-------
                       
                        "recievable_jun_2": custom_data['recievable_jun_2'],
                        "ondue_jun_2": 0,
                        "afterdue_jun_2": 0,
                        "firstmon_jun_2":0,
                        "secmon_jun_2":0,
                        "thirdmon_jun_2": 0,
                        "actual_recievable_jun_2":0,
                        "total_recieve_jun_2":0,
                        "bad_debt_jun_2": 0,
                        "percentage_bd_jun_2": 0,

                        
                        #------jul23-------
                       
                        "recievable_jul_2": custom_data['recievable_jul_2'],
                        "ondue_jul_2": 0,
                        "afterdue_jul_2": 0,
                        "firstmon_jul_2":0,
                        "secmon_jul_2":0,
                        "thirdmon_jul_2": 0,
                        "actual_recievable_jul_2":0,
                        "total_recieve_jul_2":0,
                        "bad_debt_jul_2": 0,
                        "percentage_bd_jul_2": 0,

                        
                        #------aug23-------
                       
                        "recievable_aug_2": custom_data['recievable_aug_2'],
                        "ondue_aug_2": 0,
                        "afterdue_aug_2": 0,
                        "firstmon_aug_2":0,
                        "secmon_aug_2":0,
                        "thirdmon_aug_2": 0,
                        "actual_recievable_aug_2":0,
                        "total_recieve_aug_2":0,
                        "bad_debt_aug_2": 0,
                        "percentage_bd_aug_2": 0,

                        
                        #------sep23-------
                       
                        "recievable_sep_2": custom_data['recievable_sep_2'],
                        "ondue_sep_2": 0,
                        "afterdue_sep_2": 0,
                        "firstmon_sep_2":0,
                        "secmon_sep_2":0,
                        "thirdmon_sep_2": 0,
                        "actual_recievable_sep_2":0,
                        "total_recieve_sep_2":0,
                        "bad_debt_sep_2": 0,
                        "percentage_bd_sep_2": 0,

                        
                        #------oct23-------
                       
                        "recievable_oct_2": custom_data['recievable_oct_2'],
                        "ondue_oct_2": 0,
                        "afterdue_oct_2": 0,
                        "firstmon_oct_2":0,
                        "secmon_oct_2":0,
                        "thirdmon_oct_2": 0,
                        "actual_recievable_oct_2":0,
                        "total_recieve_oct_2":0,
                        "bad_debt_oct_2": 0,
                        "percentage_bd_oct_2": 0,

                        
                        #------nov23-------
                       
                        "recievable_nov_2": custom_data['recievable_nov_2'],
                        "ondue_nov_2": 0,
                        "afterdue_nov_2": 0,
                        "firstmon_nov_2":0,
                        "secmon_nov_2":0,
                        "thirdmon_nov_2": 0,
                        "actual_recievable_nov_2":0,
                        "total_recieve_nov_2":0,
                        "bad_debt_nov_2": 0,
                        "percentage_bd_nov_2": 0,

                        
                        #------dec23-------
                       
                        "recievable_dec_2": custom_data['recievable_dec_2'],
                        "ondue_dec_2": 0,
                        "afterdue_dec_2": 0,
                        "firstmon_dec_2":0,
                        "secmon_dec_2":0,
                        "thirdmon_dec_2": 0,
                        "actual_recievable_dec_2":0,
                        "total_recieve_dec_2":0,
                        "bad_debt_dec_2": 0,
                        "percentage_bd_dec_2": 0,

                        
            
                    })
                    lines.append(mvl.id)
                    lst=[]
                    lst.append(mvl['student_branch'])
                    lst.append(mvl['student_campus'])
                    lst.append(mvl['recievable_jan_2'])
                    lst.append(mvl['recievable_mar_2'])
                    raise UserError(lst)


            
            
            
            
            self.write({
                "account_report_line":[(6,0,lines)]
            }

            )
            # raise UserError(str(final_lst))
        
       
        

        
            
    
    def action_print_excel_report(self):
        

        self.action_print_report()
        
        
        # if xlwt:

            
        #     filename = 'aging OF WITHDRAWAL STUDENTS.xls'
        #     # One sheet by partner
        #     workbook = xlwt.Workbook()
        #     # sheet = workbook.add_sheet(report_name[:31])
        #     worksheet = workbook.add_sheet('agings of Withdrawl Std')
            

            
        #     style_title = xlwt.easyxf(
        #     "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
        #     red_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour tan;'
        #     "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
        #     yellow_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
        #     "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
        #     lime_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour lime;'
        #     "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")

        #     grand_heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;'
        #                       'font: colour black, bold True;')

        #     heading_style = xlwt.easyxf('align: vertical center,horiz center;')
            
        #     date_format = xlwt.XFStyle()
        #     date_format.num_format_str = 'dd/mm/yyyy'

        #     worksheet.write_merge(0, 1, 0, 5,"LACAS SCHOOL NETWORK ",style=style_title)
        #     worksheet.write_merge(0, 1, 6, 11, "aging Report OF  STUDENTS", style=style_title)
            
            

        #     worksheet.write_merge(2,3,0,0,"Sr.No", style=red_style_title)
        #     worksheet.write_merge(2,3,1,3,"ID",style=red_style_title)
        #     worksheet.write_merge(2,3,4,5,"App Date",style=red_style_title)
        #     worksheet.write_merge(2,3,6,7,"Roll No",style=red_style_title)
        #     worksheet.write_merge(2,3,8,9,"6 Digit Roll No",style=yellow_style_title)
        #     worksheet.write_merge(2,3,10,11,"Name",style=red_style_title)
        #     worksheet.write_merge(2,3,12,13,"Batch #",style=red_style_title)
        #     worksheet.write_merge(2,3,14,16,"Branch",style=red_style_title)
        #     worksheet.write_merge(2,3,17,18,"Class",style=red_style_title)
        #     worksheet.write_merge(2,3,19,20,"withdrawn Status", red_style_title)
        #     worksheet.write_merge(2,3,21,22,"Leaving Reaon", red_style_title)
        #     worksheet.write_merge(2,3,23,24,"Remarks", red_style_title)
        #     worksheet.write_merge(2,3,25,26,"Withdrawn DT", red_style_title)


        #     v_from_month=datetime.strptime(str(self.date_from), "%Y-%m-%d").strftime('%m')
        #     v_from_year=datetime.strptime(str(self.date_from), "%Y-%m-%d").strftime('%y')

        #     v_to_month=datetime.strptime(str(self.date_to), "%Y-%m-%d").strftime('%m')
        #     v_to_year=datetime.strptime(str(self.date_to), "%Y-%m-%d").strftime('%y')

        #     months= {
        #         1:['01','JAN-22',10,'22'],
        #         2:['02','FEB-22',20,'22'],
        #         3:['03','MAR-22',30,'22'],
        #         4:['04','APR-22',40,'22'],
        #         5:['05','MAY-22',50,'22'],
        #         6:['06','JUN-22',60,'22'],
        #         7:['07','JUL-22',70,'22'],
        #         8:['08','AUG-22',80,'22'],
        #         9:['09','SEP-22',90,'22'],
        #         10:['10','OCT-22',100,'22'],
        #         11:['11','NOV-22',110,'22'],
        #         12:['12','DEC-22',120,'22'],
        #         13:['01','JAN-23',130,'23'],
        #         14:['02','FEB-23',140,'23'],
        #         15:['03','MAR-23',150,'23'],
        #         16:['04','APR-23',160,'23'],
        #         17:['05','MAY-23',170,'23'],
        #         18:['06','JUN-23',180,'23'],
        #         19:['07','JUL-23',190,'23'],
        #         20:['08','AUG-23',200,'23'],
        #         21:['09','SEP-23',200,'23'],
        #         22:['10','OCT-23',200,'23'],
        #         23:['11','NOV-23',200,'23'],
        #         24:['12','DEC-23',200,'23'],
        #         }
        #     range_start = 0
        #     range_stop = 0
        #     # raise UserError(v_to)
        #     for key, value in months.items():
        #         if value[0] == v_from_month and value[3] == v_from_year:
        #             range_start = key
        #         if value[0] == v_to_month and value[3] == v_to_year:

        #             range_stop = key

        #     col = 27
            
      
        #     for i in range(range_start,range_stop+1):
      
        #         worksheet.write_merge(2,3,col,col+1,months[i][1],red_style_title)
        #         # worksheet.write_merge(row,row,col,col+1,months[i][2])
        #         col+=2

        #     worksheet.write_merge(2,3,col,col+1,"Total", lime_style_title)   
            
        #         # print('col:',months[i][1], 'data:',months[i][2])

        #     # row = 4
        #     # sno = 1
        
        #     column = 27
        #     row = 4
        #     sn=1
        #     for rec in self.account_report_line:
                

                
        #         if rec:

        #             column = 27

        #             worksheet.write(row,0,sn)
        #             worksheet.write_merge(row,row,1,3,rec.record_id,heading_style)
        #             worksheet.write_merge(row,row,4,5,rec.app_date,heading_style)
        #             worksheet.write_merge(row,row,6,7,rec.roll_no,heading_style)
        #             worksheet.write_merge(row,row,8,9,rec.full_roll_no,heading_style)
        #             worksheet.write_merge(row,row,10,11,rec.name,heading_style)
        #             worksheet.write_merge(row,row,12,13,rec.student_batch,heading_style)
        #             worksheet.write_merge(row,row,14,16,rec.student_branch,heading_style)
        #             worksheet.write_merge(row,row,17,18,rec.student_class,heading_style)
        #             worksheet.write_merge(row,row,19,20,rec.withdrawn_status,heading_style)
        #             worksheet.write_merge(row,row,21,22,rec.leaving_reason,heading_style)
        #             worksheet.write_merge(row,row,23,24,rec.remarks,heading_style)
        #             worksheet.write_merge(row,row,25,26,rec.withdrawn_date,heading_style)

        #             data_month= {
        #                 1:['01','JAN-22',rec.jan,'22'],
        #                 2:['02','FEB-22',rec.feb,'22'],
        #                 3:['03','MAR-22',rec.mar,'22'],
        #                 4:['04','APR-22',rec.apr,'22'],
        #                 5:['05','MAY-22',rec.may,'22'],
        #                 6:['06','JUN-22',rec.jun,'22'],
        #                 7:['07','JUL-22',rec.jul,'22'],
        #                 8:['08','AUG-22',rec.aug,'22'],
        #                 9:['09','SEP-22',rec.sep,'22'],
        #                 10:['10','OCT-22',rec.oct,'22'],
        #                 11:['11','NOV-22',rec.nov,'22'],
        #                 12:['12','DEC-22',rec.dec,'22'],
        #                 13:['01','JAN-23',rec.jan_2,'23'],
        #                 14:['02','FEB-23',rec.feb_2,'23'],
        #                 15:['03','MAR-23',rec.mar_2,'23'],
        #                 16:['04','APR-23',rec.apr_2,'23'],
        #                 17:['05','MAY-23',rec.may_2,'23'],
        #                 18:['06','JUN-23',rec.jun_2,'23'],
        #                 19:['07','JUL-23',rec.jul_2,'23'],
        #                 20:['08','AUG-23',rec.aug_2,'23'],
        #                 21:['09','SEP-23',rec.sep_2,'23'],
        #                 22:['10','OCT-23',rec.oct_2,'23'],
        #                 23:['11','NOV-23',rec.nov_2,'23'],
        #                 24:['12','DEC-23',rec.dec_2,'23'],
        #             }
        #             range_start = 0
        #             range_stop = 0
                  
        #             for key, value in data_month.items():
        #                 if value[0] == v_from_month and value[3] == v_from_year:
        #                     range_start = key
        #                 if value[0] == v_to_month and value[3] == v_to_year:
        #                     range_stop = key
                    

        #             for i in range(range_start,range_stop+1):
        #                 # raise UserError(column)
        #                 worksheet.write_merge(row,row,column,column+1,data_month[i][2],heading_style)
        #                 # worksheet.write_merge(row,row,column,column+1,rec.total_amount)
        #                 # lst.append([row_1,row_1,column,column+1])
                      
        #                 column+=2
        #             worksheet.write_merge(row,row,column,column+1,rec.total_amount,heading_style)
                      
        #             row+=1
        #             sn+=1

        #     fp = io.BytesIO()
        #     workbook.save(fp)

        #     export_id = self.env['sale.day.book.report.excel'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        #     res = {
        #             'view_mode': 'form',
        #             'res_id': export_id.id,
        #             'res_model': 'sale.day.book.report.excel',
        #             'type': 'ir.actions.act_window',
        #             'target':'new'
        #         }
        #     return res
            
        # else:
        #     raise Warning (""" You Don't have xlwt library.\n Please install it by executing this command :  sudo pip3 install xlwt""")
        

   
                

           

























