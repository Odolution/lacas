
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
import xlsxwriter
_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
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
    percentage_bdb_jan=fields.Char('JAN-22')


  
    recievable_feb=fields.Integer('FEB-22')
    ondue_feb=fields.Integer('FEB-22')
    afterdue_feb=fields.Integer('FEB-22')
    firstmon_feb=fields.Integer('FEB-22')
    secmon_feb=fields.Integer('FEB-22')
    thirdmon_feb=fields.Integer('FEB-22')
    actual_recievable_feb=fields.Integer('FEB-22')
    total_recieve_feb=fields.Integer('FEB-22')
    bad_debt_feb=fields.Integer('FEB-22')
    percentage_bdb_feb=fields.Char('FEB-22')


    recievable_mar=fields.Integer('MAR-22')
    ondue_mar=fields.Integer('MAR-22')
    afterdue_mar=fields.Integer('MAR-22')
    firstmon_mar=fields.Integer('MAR-22')
    secmon_mar=fields.Integer('MAR-22')
    thirdmon_mar=fields.Integer('MAR-22')
    actual_recievable_mar=fields.Integer('MAR-22')
    total_recieve_mar=fields.Integer('MAR-22')
    bad_debt_mar=fields.Integer('MAR-22')
    percentage_bdb_mar=fields.Char('MAR-22')

    recievable_apr=fields.Integer('APR-22')
    ondue_apr=fields.Integer('APR-22')
    afterdue_apr=fields.Integer('APR-22')
    firstmon_apr=fields.Integer('APR-22')
    secmon_apr=fields.Integer('APR-22')
    thirdmon_apr=fields.Integer('APR-22')
    actual_recievable_apr=fields.Integer('APR-22')
    total_recieve_apr=fields.Integer('APR-22')
    bad_debt_apr=fields.Integer('APR-22')
    percentage_bdb_apr=fields.Char('APR-22')

    recievable_may=fields.Integer('MAY-22')
    ondue_may=fields.Integer('MAY-22')
    afterdue_may=fields.Integer('MAY-22')
    firstmon_may=fields.Integer('MAY-22')
    secmon_may=fields.Integer('MAY-22')
    thirdmon_may=fields.Integer('MAY-22')
    actual_recievable_may=fields.Integer('MAY-22')
    total_recieve_may=fields.Integer('MAY-22')
    bad_debt_may=fields.Integer('MAY-22')
    percentage_bdb_may=fields.Char('MAY-22')

    recievable_jun=fields.Integer('JUN-22')
    ondue_jun=fields.Integer('JUN-22')
    afterdue_jun=fields.Integer('JUN-22')
    firstmon_jun=fields.Integer('JUN-22')
    secmon_jun=fields.Integer('JUN-22')
    thirdmon_jun=fields.Integer('JUN-22')
    actual_recievable_jun=fields.Integer('JUN-22')
    total_recieve_jun=fields.Integer('JUN-22')
    bad_debt_jun=fields.Integer('JUN-22')
    percentage_bdb_jun=fields.Char('JUN-22')

    recievable_jul=fields.Integer('JUL-22')
    ondue_jul=fields.Integer('JUL-22')
    afterdue_jul=fields.Integer('JUL-22')
    firstmon_jul=fields.Integer('JUL-22')
    secmon_jul=fields.Integer('JUL-22')
    thirdmon_jul=fields.Integer('JUL-22')
    actual_recievable_jul=fields.Integer('JUL-22')
    total_recieve_jul=fields.Integer('JUL-22')
    bad_debt_jul=fields.Integer('JUL-22')
    percentage_bdb_jul=fields.Char('JUL-22')

    recievable_aug=fields.Integer('AUG-22')
    ondue_aug=fields.Integer('AUG-22')
    afterdue_aug=fields.Integer('AUG-22')
    firstmon_aug=fields.Integer('AUG-22')
    secmon_aug=fields.Integer('AUG-22')
    thirdmon_aug=fields.Integer('AUG-22')
    actual_recievable_aug=fields.Integer('AUG-22')
    total_recieve_aug=fields.Integer('AUG-22')
    bad_debt_aug=fields.Integer('AUG-22')
    percentage_bdb_aug=fields.Char('AUG-22')

    recievable_sep=fields.Integer('SEP-22')
    ondue_sep=fields.Integer('SEP-22')
    afterdue_sep=fields.Integer('SEP-22')
    firstmon_sep=fields.Integer('SEP-22')
    secmon_sep=fields.Integer('SEP-22')
    thirdmon_sep=fields.Integer('SEP-22')
    actual_recievable_sep=fields.Integer('SEP-22')
    total_recieve_sep=fields.Integer('SEP-22')
    bad_debt_sep=fields.Integer('SEP-22')
    percentage_bdb_sep=fields.Char('SEP-22')

    recievable_oct=fields.Integer('OCT-22')
    ondue_oct=fields.Integer('OCT-22')
    afterdue_oct=fields.Integer('OCT-22')
    firstmon_oct=fields.Integer('OCT-22')
    secmon_oct=fields.Integer('OCT-22')
    thirdmon_oct=fields.Integer('OCT-22')
    actual_recievable_oct=fields.Integer('OCT-22')
    total_recieve_oct=fields.Integer('OCT-22')
    bad_debt_oct=fields.Integer('OCT-22')
    percentage_bdb_oct=fields.Char('OCT-22')

    recievable_nov=fields.Integer('NOV-22')
    ondue_nov=fields.Integer('NOV-22')
    afterdue_nov=fields.Integer('NOV-22')
    firstmon_nov=fields.Integer('NOV-22')
    secmon_nov=fields.Integer('NOV-22')
    thirdmon_nov=fields.Integer('NOV-22')
    actual_recievable_nov=fields.Integer('NOV-22')
    total_recieve_nov=fields.Integer('NOV-22')
    bad_debt_nov=fields.Integer('NOV-22')
    percentage_bdb_nov=fields.Char('NOV-22')

    recievable_dec=fields.Integer('DEC-22')
    ondue_dec=fields.Integer('DEC-22')
    afterdue_dec=fields.Integer('DEC-22')
    firstmon_dec=fields.Integer('DEC-22')
    secmon_dec=fields.Integer('DEC-22')
    thirdmon_dec=fields.Integer('DEC-22')
    actual_recievable_dec=fields.Integer('DEC-22')
    total_recieve_dec=fields.Integer('DEC-22')
    bad_debt_dec=fields.Integer('DEC-22')
    percentage_bdb_dec=fields.Char('DEC-22')

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
    percentage_bdb_jan_2=fields.Char('JAN-23')


  
    recievable_feb_2=fields.Integer('FEB-23')
    ondue_feb_2=fields.Integer('FEB-23')
    afterdue_feb_2=fields.Integer('FEB-23')
    firstmon_feb_2=fields.Integer('FEB-23')
    secmon_feb_2=fields.Integer('FEB-23')
    thirdmon_feb_2=fields.Integer('FEB-23')
    actual_recievable_feb_2=fields.Integer('FEB-23')
    total_recieve_feb_2=fields.Integer('FEB-23')
    bad_debt_feb_2=fields.Integer('FEB-23')
    percentage_bdb_feb_2=fields.Char('FEB-23')


    recievable_mar_2=fields.Integer('MAR-23')
    ondue_mar_2=fields.Integer('MAR-23')
    afterdue_mar_2=fields.Integer('MAR-23')
    firstmon_mar_2=fields.Integer('MAR-23')
    secmon_mar_2=fields.Integer('MAR-23')
    thirdmon_mar_2=fields.Integer('MAR-23')
    actual_recievable_mar_2=fields.Integer('MAR-23')
    total_recieve_mar_2=fields.Integer('MAR-23')
    bad_debt_mar_2=fields.Integer('MAR-23')
    percentage_bdb_mar_2=fields.Char('MAR-23')

    recievable_apr_2=fields.Integer('APR-23')
    ondue_apr_2=fields.Integer('APR-23')
    afterdue_apr_2=fields.Integer('APR-23')
    firstmon_apr_2=fields.Integer('APR-23')
    secmon_apr_2=fields.Integer('APR-23')
    thirdmon_apr_2=fields.Integer('APR-23')
    actual_recievable_apr_2=fields.Integer('APR-23')
    total_recieve_apr_2=fields.Integer('APR-23')
    bad_debt_apr_2=fields.Integer('APR-23')
    percentage_bdb_apr_2=fields.Char('APR-23')

    recievable_may_2=fields.Integer('MAY-23')
    ondue_may_2=fields.Integer('MAY-23')
    afterdue_may_2=fields.Integer('MAY-23')
    firstmon_may_2=fields.Integer('MAY-23')
    secmon_may_2=fields.Integer('MAY-23')
    thirdmon_may_2=fields.Integer('MAY-23')
    actual_recievable_may_2=fields.Integer('MAY-23')
    total_recieve_may_2=fields.Integer('MAY-23')
    bad_debt_may_2=fields.Integer('MAY-23')
    percentage_bdb_may_2=fields.Char('MAY-23')

    recievable_jun_2=fields.Integer('JUN-23')
    ondue_jun_2=fields.Integer('JUN-23')
    afterdue_jun_2=fields.Integer('JUN-23')
    firstmon_jun_2=fields.Integer('JUN-23')
    secmon_jun_2=fields.Integer('JUN-23')
    thirdmon_jun_2=fields.Integer('JUN-23')
    actual_recievable_jun_2=fields.Integer('JUN-23')
    total_recieve_jun_2=fields.Integer('JUN-23')
    bad_debt_jun_2=fields.Integer('JUN-23')
    percentage_bdb_jun_2=fields.Char('JUN-23')

    recievable_jul_2=fields.Integer('JUL-23')
    ondue_jul_2=fields.Integer('JUL-23')
    afterdue_jul_2=fields.Integer('JUL-23')
    firstmon_jul_2=fields.Integer('JUL-23')
    secmon_jul_2=fields.Integer('JUL-23')
    thirdmon_jul_2=fields.Integer('JUL-23')
    actual_recievable_jul_2=fields.Integer('JUL-23')
    total_recieve_jul_2=fields.Integer('JUL-23')
    bad_debt_jul_2=fields.Integer('JUL-23')
    percentage_bdb_jul_2=fields.Char('JUL-23')

    recievable_aug_2=fields.Integer('AUG-23')
    ondue_aug_2=fields.Integer('AUG-23')
    afterdue_aug_2=fields.Integer('AUG-23')
    firstmon_aug_2=fields.Integer('AUG-23')
    secmon_aug_2=fields.Integer('AUG-23')
    thirdmon_aug_2=fields.Integer('AUG-23')
    actual_recievable_aug_2=fields.Integer('AUG-23')
    total_recieve_aug_2=fields.Integer('AUG-23')
    bad_debt_aug_2=fields.Integer('AUG-23')
    percentage_bdb_aug_2=fields.Char('AUG-23')

    recievable_sep_2=fields.Integer('SEP-23')
    ondue_sep_2=fields.Integer('SEP-23')
    afterdue_sep_2=fields.Integer('SEP-23')
    firstmon_sep_2=fields.Integer('SEP-23')
    secmon_sep_2=fields.Integer('SEP-23')
    thirdmon_sep_2=fields.Integer('SEP-23')
    actual_recievable_sep_2=fields.Integer('SEP-23')
    total_recieve_sep_2=fields.Integer('SEP-23')
    bad_debt_sep_2=fields.Integer('SEP-23')
    percentage_bdb_sep_2=fields.Char('SEP-23')

    recievable_oct_2=fields.Integer('OCT-23')
    ondue_oct_2=fields.Integer('OCT-23')
    afterdue_oct_2=fields.Integer('OCT-23')
    firstmon_oct_2=fields.Integer('OCT-23')
    secmon_oct_2=fields.Integer('OCT-23')
    thirdmon_oct_2=fields.Integer('OCT-23')
    actual_recievable_oct_2=fields.Integer('OCT-23')
    total_recieve_oct_2=fields.Integer('OCT-23')
    bad_debt_oct_2=fields.Integer('OCT-23')
    percentage_bdb_oct_2=fields.Char('OCT-23')

    recievable_nov_2=fields.Integer('NOV-23')
    ondue_nov_2=fields.Integer('NOV-23')
    afterdue_nov_2=fields.Integer('NOV-23')
    firstmon_nov_2=fields.Integer('NOV-23')
    secmon_nov_2=fields.Integer('NOV-23')
    thirdmon_nov_2=fields.Integer('NOV-23')
    actual_recievable_nov_2=fields.Integer('NOV-23')
    total_recieve_nov_2=fields.Integer('NOV-23')
    bad_debt_nov_2=fields.Integer('NOV-23')
    percentage_bdb_nov_2=fields.Char('NOV-23')

    recievable_dec_2=fields.Integer('DEC-23')
    ondue_dec_2=fields.Integer('DEC-23')
    afterdue_dec_2=fields.Integer('DEC-23')
    firstmon_dec_2=fields.Integer('DEC-23')
    secmon_dec_2=fields.Integer('DEC-23')
    thirdmon_dec_2=fields.Integer('DEC-23')
    actual_recievable_dec_2=fields.Integer('DEC-23')
    total_recieve_dec_2=fields.Integer('DEC-23')
    bad_debt_dec_2=fields.Integer('DEC-23')
    percentage_bdb_dec_2=fields.Char('DEC-23')


    
   

class agingsReportWizard(models.TransientModel):
    _name="aging.report.wizard"
    _description='Print aging Wizard'

    date_from=fields.Date(string="Date From")
    date_to=fields.Date(string="Date To")

    account_report_line=fields.Many2many('account.aging.move.line', string='Account report Line')
    groups_ids = fields.Many2many('aging.invoice.group', string='Groups')

    def _date_constrains(self):
        if not self.date_to or not self.date_from:
            raise UserError("Sorry, you must enter both dates..")
        
        
        if not self.date_from and not self.date_to :
            raise UserError("Sorry, you must enter dates..")
        
        else:

            from_year=datetime.strptime(str(self.date_from), "%Y-%m-%d").strftime('%y')
            to_year=datetime.strptime(str(self.date_to), "%Y-%m-%d").strftime('%y')
            # raise UserError(from_year)

            if self.date_to < self.date_from:
                # raise UserError(datetime.strptime(str(self.date_from), "%Y-%m-%d").strftime('%y'))

                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

            if from_year and to_year :

                if  from_year < '22' or from_year >'23':
                    raise UserError("Sorry, Year must be between 2022-2023..")
                    raise ValidationError(_('Sorry, Year must be 2022-2023...'))

                elif to_year <"22" or to_year >"23":
                    raise UserError("Sorry, Year must be between 2022-2023..")
                    raise ValidationError(_('Sorry, Year must be 2022-2023...'))



  
    
    def action_print_report(self):

        

        # move_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('journal_id','=',125),("invoice_date",">=",self.date_from),("invoice_date","<=",self.date_to)])
        move_ids=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),("invoice_date",">=",self.date_from),("invoice_date","<=",self.date_to)])
        branch_lst=[]

        for inv in move_ids:
            if inv.x_studio_previous_branch!=False:
                if inv.x_studio_previous_branch not in branch_lst :
                    campus=inv.x_studio_previous_branch
                    branch_lst.append(str(campus))

        lines=[]
        _logger.info(f"branch: {branch_lst}")



        for branch in branch_lst:
            _logger.info(f"loop: {branch}")

           
            # branch_wise_inv=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('x_studio_previous_branch','=',branch.id),('journal_id','=',125),("invoice_date",">=",self.date_from),("invoice_date","<=",self.date_to)])
            branch_wise_inv=self.env['account.move'].search([('move_type','=','out_invoice'),('state','=','posted'),('x_studio_previous_branch','=',branch),("invoice_date",">=",self.date_from),("invoice_date","<=",self.date_to)])
            _logger.info(f"invoices length: {len(branch_wise_inv)}")
            
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
                        "percentage_bdb_jan": '',

                        
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
                        "percentage_bdb_feb": '',

                        
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
                        "percentage_bdb_mar": '',

                        
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
                        "percentage_bdb_apr": '',

                        
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
                        "percentage_bdb_may": '',

                        
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
                        "percentage_bdb_jun": '',

                        
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
                        "percentage_bdb_jul": '',

                        
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
                        "percentage_bd_aug": '',

                        
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
                        "percentage_bdb_sep": '',

                        
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
                        "percentage_bd_oct": '',

                        
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
                        "percentage_bd_nov": '',

                        
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
                        "percentage_bdb_dec": '',

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
                        "percentage_bdb_jan_2": '',

                        
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
                        "percentage_bdb_feb_2": '',

                        
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
                        "percentage_bdb_mar_2": '',

                        
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
                        "percentage_bdb_apr_2": '',

                        
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
                        "percentage_bdb_may_2": '',

                        
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
                        "percentage_bdb_jun_2": '',

                        
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
                        "percentage_bdb_jul_2": '',

                        
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
                        "percentage_bdb_aug_2": '',

                        
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
                        "percentage_bdb_sep_2": '',

                        
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
                        "percentage_bdb_oct_2": '',

                        
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
                        "percentage_bdb_nov_2": '',

                        
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
                        "percentage_bdb_dec_2": '',

                    } 

            custom_data['student_branch'] = branch
            custom_data['student_campus'] = branch

            for value in branch_wise_inv:
                # if value.x_studio_previous_branch==branch:

                    

                # custom_data['student_branch'] = value.x_studio_previous_branch.display_name if  len(value.x_studio_previous_branch)==1  else ""
                # custom_data['student_campus'] = value.campus if value.campus else ''

                if value.month_date == "January" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_jan'] += value.due_amount
                        _logger.info(f"recievable_jan: {custom_data['recievable_jan']}")
                        
                    if value.payment_state=='paid':
                        custom_data['recievable_jan'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_jan'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_jan'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_jan'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_jan'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_jan'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_jan'] += (int(value.bill_amount))



                elif value.month_date == "Feburary" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_feb'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_feb'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_feb'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_feb'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_feb'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_feb'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_feb'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_feb'] += (int(value.bill_amount))

                elif value.month_date == "March"and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_mar'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_mar'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_mar'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_mar'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_mar'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_mar'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_mar'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_mar'] += (int(value.bill_amount))


                elif value.month_date == "April" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_apr'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_apr'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_apr'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_apr'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_apr'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_apr'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_apr'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_apr'] += (int(value.bill_amount))


                elif value.month_date == "May" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_may'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_may'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_may'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_may'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_may'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_may'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_may'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_may'] += (int(value.bill_amount))


                elif value.month_date == "June" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_jun'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_jun'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_jun'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_jun'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_jun'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_jun'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_jun'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_jun'] += (int(value.bill_amount))


                elif value.month_date == "July" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_jul'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_jul'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_jul'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_jul'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_jul'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_jul'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_jul'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_jul'] += (int(value.bill_amount))


                elif value.month_date == "August" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_aug'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_aug'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_aug'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_aug'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_aug'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_aug'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_aug'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_aug'] += (int(value.bill_amount))

                elif value.month_date == "September" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_sep'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_sep'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_sep'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_sep'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_sep'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_sep'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_sep'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_sep'] += (int(value.bill_amount))

                elif value.month_date == "October" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_oct'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_oct'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_oct'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_oct'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_oct'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_oct'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_oct'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_oct'] += (int(value.bill_amount))


                elif value.month_date == "November" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_nov'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_nov'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_nov'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_nov'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_nov'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_nov'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_nov'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_nov'] += (int(value.bill_amount))


                elif value.month_date == "December" and value.year_date=='22':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_dec'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_dec'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_dec'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_dec'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_dec'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_dec'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_dec'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_dec'] += (int(value.bill_amount))


                elif value.month_date == "January" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_jan_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_jan_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_jan_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_jan_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_jan_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_jan_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_jan_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_jan_2'] += (int(value.bill_amount))



                elif value.month_date == "Feburary" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_feb_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_feb_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_feb_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_feb_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_feb_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_feb_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_feb_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_feb_2'] += (int(value.bill_amount))


                elif value.month_date == "March"and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_mar_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_mar_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_mar_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_mar_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_mar_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_mar_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_mar_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_mar_2'] += (int(value.bill_amount))



                elif value.month_date == "April" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_apr_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_apr_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_apr_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_apr_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_apr_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_apr_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_apr_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_apr_2'] += (int(value.bill_amount))


                elif value.month_date == "May" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_may_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_may_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_may_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_may_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_may_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_may_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_may_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_may_2'] += (int(value.bill_amount))


                elif value.month_date == "June" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_jun_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_jun_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_jun_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_jun_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_jun_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_jun_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_jun_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_jun_2'] += (int(value.bill_amount))


                elif value.month_date == "July" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_jul_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_jul_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_jul_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_jul_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_jul_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_jul_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_jul_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_jul_2'] += (int(value.bill_amount))

                elif value.month_date == "August" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_aug_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_aug_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_aug_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_aug_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_aug_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_aug_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_aug_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_aug_2'] += (int(value.bill_amount))


                elif value.month_date == "September" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_sep_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_sep_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_sep_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_sep_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_sep_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_sep_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_sep_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_sep_2'] += (int(value.bill_amount))


                elif value.month_date == "October" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_oct_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_oct_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_oct_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_oct_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_oct_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_oct_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_oct_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_oct_2'] += (int(value.bill_amount))

                elif value.month_date == "November" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_nov_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_nov_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_nov_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_nov_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_nov_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_nov_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_nov_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_nov_2'] += (int(value.bill_amount))

                elif value.month_date == "December" and value.year_date=='23':
                    if value.payment_state=='not_paid':
                        custom_data['recievable_dec_2'] += value.due_amount
                    if value.payment_state=='paid':
                        custom_data['recievable_dec_2'] += (int(value.bill_amount))
                        if value.ol_payment_date:
                            first_date=value.invoice_date.replace(day=1)
                            diff=value.ol_payment_date-first_date
                            if diff.days >0 and diff.days<11:
                                custom_data['ondue_dec_2'] += (int(value.bill_amount))
                            if diff.days >10 and diff.days<31:
                                custom_data['afterdue_dec_2'] += (int(value.bill_amount))
                            if diff.days>30 and diff.days<61:
                                custom_data['firstmon_dec_2'] += (int(value.bill_amount))
                            if diff.days>60 and diff.days<91:
                                custom_data['secmon_dec_2'] += (int(value.bill_amount))
                            if diff.days>90 and diff.days<121:
                                custom_data['thirdmon_dec_2'] += (int(value.bill_amount))
                            if diff.days>120:
                                custom_data['actual_recievable_dec_2'] += (int(value.bill_amount))

            tr_jan=custom_data['ondue_jan']+custom_data['afterdue_jan']+ custom_data['firstmon_jan']+custom_data['secmon_jan']+custom_data['thirdmon_jan']+ custom_data['actual_recievable_jan']
            bd_jan=custom_data['recievable_jan']-tr_jan
            bd_perc_jan=0
            if custom_data['recievable_jan']!=0:
                bd_perc_jan=bd_jan/custom_data['recievable_jan']*100
            

            tr_feb=custom_data['ondue_feb']+custom_data['afterdue_feb']+ custom_data['firstmon_feb']+custom_data['secmon_feb']+custom_data['thirdmon_feb']+ custom_data['actual_recievable_feb']
            bd_feb=custom_data['recievable_feb']-tr_feb
            bd_perc_feb=0
            if custom_data['recievable_feb']!=0:
                bd_perc_feb=bd_feb/custom_data['recievable_feb']*100

            tr_mar=custom_data['ondue_mar']+custom_data['afterdue_mar']+ custom_data['firstmon_mar']+custom_data['secmon_mar']+custom_data['thirdmon_mar']+ custom_data['actual_recievable_mar']
            bd_mar=custom_data['recievable_mar']-tr_mar
            bd_perc_mar=0
            if custom_data['recievable_mar']!=0:
                bd_perc_mar=bd_mar/custom_data['recievable_mar']*100

            tr_apr=custom_data['ondue_apr']+custom_data['afterdue_apr']+ custom_data['firstmon_apr']+custom_data['secmon_apr']+custom_data['thirdmon_apr']+ custom_data['actual_recievable_apr']
            bd_apr=custom_data['recievable_apr']-tr_apr
            bd_perc_apr=0
            if custom_data['recievable_apr']!=0:
                bd_perc_apr=bd_apr/custom_data['recievable_apr']*100

            tr_may=custom_data['ondue_may']+custom_data['afterdue_may']+ custom_data['firstmon_may']+custom_data['secmon_may']+custom_data['thirdmon_may']+ custom_data['actual_recievable_may']
            bd_may=custom_data['recievable_may']-tr_may
            bd_perc_may=0
            if custom_data['recievable_may']!=0:
                bd_perc_may=bd_may/custom_data['recievable_may']*100

            tr_jun=custom_data['ondue_jun']+custom_data['afterdue_jun']+ custom_data['firstmon_jun']+custom_data['secmon_jun']+custom_data['thirdmon_jun']+ custom_data['actual_recievable_jun']
            bd_jun=custom_data['recievable_jun']-tr_jun
            bd_perc_jun=0
            if custom_data['recievable_jun']!=0:
                bd_perc_jun=bd_jun/custom_data['recievable_jun']*100

            tr_jul=custom_data['ondue_jul']+custom_data['afterdue_jul']+ custom_data['firstmon_jul']+custom_data['secmon_jul']+custom_data['thirdmon_jul']+ custom_data['actual_recievable_jul']
            bd_jul=custom_data['recievable_jul']-tr_jul
            bd_perc_jul=0
            if custom_data['recievable_jul']!=0:
                bd_perc_jul=bd_jul/custom_data['recievable_jul']*100

            tr_aug=custom_data['ondue_aug']+custom_data['afterdue_aug']+ custom_data['firstmon_aug']+custom_data['secmon_aug']+custom_data['thirdmon_aug']+ custom_data['actual_recievable_aug']
            bd_aug=custom_data['recievable_aug']-tr_aug
            bd_perc_aug=0
            if custom_data['recievable_aug']!=0:
                bd_perc_aug=bd_aug/custom_data['recievable_aug']*100

            tr_sep=custom_data['ondue_sep']+custom_data['afterdue_sep']+ custom_data['firstmon_sep']+custom_data['secmon_sep']+custom_data['thirdmon_sep']+ custom_data['actual_recievable_sep']
            bd_sep=custom_data['recievable_sep']-tr_sep
            bd_perc_sep=0
            if custom_data['recievable_sep']!=0:
                bd_perc_sep=bd_sep/custom_data['recievable_sep']*100

            tr_oct=custom_data['ondue_oct']+custom_data['afterdue_oct']+ custom_data['firstmon_oct']+custom_data['secmon_oct']+custom_data['thirdmon_oct']+ custom_data['actual_recievable_oct']
            bd_oct=custom_data['recievable_oct']-tr_oct
            bd_perc_oct=0
            if custom_data['recievable_oct']!=0:
                bd_perc_oct=bd_oct/custom_data['recievable_oct']*100

            tr_nov=custom_data['ondue_nov']+custom_data['afterdue_nov']+ custom_data['firstmon_nov']+custom_data['secmon_nov']+custom_data['thirdmon_nov']+ custom_data['actual_recievable_nov']
            bd_nov=custom_data['recievable_nov']-tr_nov
            bd_perc_nov=0
            if custom_data['recievable_nov']!=0:
                bd_perc_nov=bd_nov/custom_data['recievable_nov']*100

            tr_dec=custom_data['ondue_dec']+custom_data['afterdue_dec']+ custom_data['firstmon_dec']+custom_data['secmon_dec']+custom_data['thirdmon_dec']+ custom_data['actual_recievable_dec']
            bd_dec=custom_data['recievable_dec']-tr_dec
            bd_perc_dec=0
            if custom_data['recievable_dec']!=0:
                bd_perc_dec=bd_dec/custom_data['recievable_dec']*100

            
            
            tr_jan_2=custom_data['ondue_jan_2']+custom_data['afterdue_jan_2']+ custom_data['firstmon_jan_2']+custom_data['secmon_jan_2']+custom_data['thirdmon_jan_2']+ custom_data['actual_recievable_jan_2']
            bd_jan_2=custom_data['recievable_jan_2']-tr_jan_2
            bd_perc_jan_2=0
            if custom_data['recievable_jan_2']!=0:
                bd_perc_jan_2=bd_jan_2/custom_data['recievable_jan_2']*100


            tr_feb_2=custom_data['ondue_feb_2']+custom_data['afterdue_feb_2']+ custom_data['firstmon_feb_2']+custom_data['secmon_feb_2']+custom_data['thirdmon_feb_2']+ custom_data['actual_recievable_feb_2']
            bd_feb_2=custom_data['recievable_feb_2']-tr_feb_2
            bd_perc_feb_2=0
            if custom_data['recievable_feb_2']!=0:
                bd_perc_feb_2=bd_feb_2/custom_data['recievable_feb_2']*100

            tr_mar_2=custom_data['ondue_mar_2']+custom_data['afterdue_mar_2']+ custom_data['firstmon_mar_2']+custom_data['secmon_mar_2']+custom_data['thirdmon_mar_2']+ custom_data['actual_recievable_mar_2']
            bd_mar_2=custom_data['recievable_mar_2']-tr_mar_2
            bd_perc_mar_2=0
            if custom_data['recievable_mar_2']!=0:
                bd_perc_mar_2=bd_mar_2/custom_data['recievable_mar_2']*100

            tr_apr_2=custom_data['ondue_apr_2']+custom_data['afterdue_apr_2']+ custom_data['firstmon_apr_2']+custom_data['secmon_apr_2']+custom_data['thirdmon_apr_2']+ custom_data['actual_recievable_apr_2']
            bd_apr_2=custom_data['recievable_apr_2']-tr_apr_2
            bd_perc_apr_2=0
            if custom_data['recievable_apr_2']!=0:
                bd_perc_apr_2=bd_apr_2/custom_data['recievable_apr_2']*100

            tr_may_2=custom_data['ondue_may_2']+custom_data['afterdue_may_2']+ custom_data['firstmon_may_2']+custom_data['secmon_may_2']+custom_data['thirdmon_may_2']+ custom_data['actual_recievable_may_2']
            bd_may_2=custom_data['recievable_may_2']-tr_may_2
            bd_perc_may_2=0
            if custom_data['recievable_may_2']!=0:
                bd_perc_may_2=bd_may_2/custom_data['recievable_may_2']*100

            tr_jun_2=custom_data['ondue_jun_2']+custom_data['afterdue_jun_2']+ custom_data['firstmon_jun_2']+custom_data['secmon_jun_2']+custom_data['thirdmon_jun_2']+ custom_data['actual_recievable_jun_2']
            bd_jun_2=custom_data['recievable_jun_2']-tr_jun_2
            bd_perc_jun_2=0
            if custom_data['recievable_jun_2']!=0:
                bd_perc_jun_2=bd_jun_2/custom_data['recievable_jun_2']*100

            tr_jul_2=custom_data['ondue_jul_2']+custom_data['afterdue_jul_2']+ custom_data['firstmon_jul_2']+custom_data['secmon_jul_2']+custom_data['thirdmon_jul_2']+ custom_data['actual_recievable_jul_2']
            bd_jul_2=custom_data['recievable_jul_2']-tr_jul_2
            bd_perc_jul_2=0
            if custom_data['recievable_jul_2']!=0:
                bd_perc_jul_2=bd_jul_2/custom_data['recievable_jul_2']*100

            tr_aug_2=custom_data['ondue_aug_2']+custom_data['afterdue_aug_2']+ custom_data['firstmon_aug_2']+custom_data['secmon_aug_2']+custom_data['thirdmon_aug_2']+ custom_data['actual_recievable_aug_2']
            bd_aug_2=custom_data['recievable_aug_2']-tr_aug_2
            bd_perc_aug_2=0
            if custom_data['recievable_aug_2']!=0:
                bd_perc_aug_2=bd_aug_2/custom_data['recievable_aug_2']*100

            tr_sep_2=custom_data['ondue_sep_2']+custom_data['afterdue_sep_2']+ custom_data['firstmon_sep_2']+custom_data['secmon_sep_2']+custom_data['thirdmon_sep_2']+ custom_data['actual_recievable_sep_2']
            bd_sep_2=custom_data['recievable_sep_2']-tr_sep_2
            bd_perc_sep_2=0
            if custom_data['recievable_sep_2']!=0:
                bd_perc_sep_2=bd_sep_2/custom_data['recievable_sep_2']*100

            tr_oct_2=custom_data['ondue_oct_2']+custom_data['afterdue_oct_2']+ custom_data['firstmon_oct_2']+custom_data['secmon_oct_2']+custom_data['thirdmon_oct_2']+ custom_data['actual_recievable_oct_2']
            bd_oct_2=custom_data['recievable_oct_2']-tr_oct_2
            bd_perc_oct_2=0
            if custom_data['recievable_oct_2']!=0:
                bd_perc_oct_2=bd_oct_2/custom_data['recievable_oct_2']*100

            tr_nov_2=custom_data['ondue_nov_2']+custom_data['afterdue_nov_2']+ custom_data['firstmon_nov_2']+custom_data['secmon_nov_2']+custom_data['thirdmon_nov_2']+ custom_data['actual_recievable_nov_2']
            bd_nov_2=custom_data['recievable_nov_2']-tr_nov_2
            bd_perc_nov_2=0
            if custom_data['recievable_nov_2']!=0:
                bd_perc_nov_2=bd_nov_2/custom_data['recievable_nov_2']*100

            tr_dec_2=custom_data['ondue_dec_2']+custom_data['afterdue_dec_2']+ custom_data['firstmon_dec_2']+custom_data['secmon_dec_2']+custom_data['thirdmon_dec_2']+ custom_data['actual_recievable_dec_2']
            bd_dec_2=custom_data['recievable_dec_2']-tr_dec_2
            bd_perc_dec_2=0
            if custom_data['recievable_dec_2']!=0:
                bd_perc_dec_2=bd_dec_2/custom_data['recievable_dec_2']*100




            mvl=self.env['account.aging.move.line'].create({
                
                "student_branch":custom_data['student_branch'],
                "student_campus":custom_data['student_campus'],
                #------jan22-------

                "recievable_jan": custom_data['recievable_jan'],
                "ondue_jan": custom_data['ondue_jan'],
                "afterdue_jan": custom_data['afterdue_jan'],
                "firstmon_jan":custom_data['firstmon_jan'],
                "secmon_jan":custom_data['secmon_jan'],
                "thirdmon_jan": custom_data['thirdmon_jan'],
                "actual_recievable_jan":custom_data['actual_recievable_jan'],
                "total_recieve_jan":tr_jan,
                "bad_debt_jan": bd_jan,
                "percentage_bdb_jan": str(bd_perc_jan)+'%' ,

                
                #------feb22-------
                
                "recievable_feb": custom_data['recievable_feb'],
                "ondue_feb": custom_data['ondue_feb'],
                "afterdue_feb": custom_data['afterdue_feb'],
                "firstmon_feb":custom_data['firstmon_feb'],
                "secmon_feb":custom_data['secmon_feb'],
                "thirdmon_feb": custom_data['thirdmon_feb'],
                "actual_recievable_feb":custom_data['actual_recievable_feb'],
                "total_recieve_feb":tr_feb,
                "bad_debt_feb": bd_feb,
                "percentage_bdb_feb": str(bd_perc_feb)+'%',

                
                #------mar22-------
                
                "recievable_mar": custom_data['recievable_mar'],
                "ondue_mar": custom_data['ondue_mar'],
                "afterdue_mar": custom_data['afterdue_mar'],
                "firstmon_mar":custom_data['firstmon_mar'],
                "secmon_mar":custom_data['secmon_mar'],
                "thirdmon_mar": custom_data['thirdmon_mar'],
                "actual_recievable_mar":custom_data['actual_recievable_mar'],
                "total_recieve_mar":tr_mar,
                "bad_debt_mar": bd_mar,
                "percentage_bdb_mar": str(bd_perc_mar)+'%',

                
                #------apr22-------
                

                "recievable_apr": custom_data['recievable_apr'],
                "ondue_apr": custom_data['ondue_apr'],
                "afterdue_apr": custom_data['afterdue_apr'],
                "firstmon_apr":custom_data['firstmon_apr'],
                "secmon_apr":custom_data['secmon_apr'],
                "thirdmon_apr": custom_data['thirdmon_apr'],
                "actual_recievable_apr":custom_data['actual_recievable_apr'],
                "total_recieve_apr":tr_apr,
                "bad_debt_apr": bd_apr,
                "percentage_bdb_apr": str(bd_perc_apr)+'%',

                

                
                #------may22-------
                

                "recievable_may": custom_data['recievable_may'],
                "ondue_may": custom_data['ondue_may'],
                "afterdue_may": custom_data['afterdue_may'],
                "firstmon_may":custom_data['firstmon_may'],
                "secmon_may":custom_data['secmon_may'],
                "thirdmon_may": custom_data['thirdmon_may'],
                "actual_recievable_may":custom_data['actual_recievable_may'],
                "total_recieve_may":tr_may,
                "bad_debt_may": bd_may,
                "percentage_bdb_may": str(bd_perc_may)+'%',

                

                
                #------jun22-------
                

                "recievable_jun": custom_data['recievable_jun'],
                "ondue_jun": custom_data['ondue_jun'],
                "afterdue_jun": custom_data['afterdue_jun'],
                "firstmon_jun":custom_data['firstmon_jun'],
                "secmon_jun":custom_data['secmon_jun'],
                "thirdmon_jun": custom_data['thirdmon_jun'],
                "actual_recievable_jun":custom_data['actual_recievable_jun'],
                "total_recieve_jun":tr_jun,
                "bad_debt_jun": bd_jun,
                "percentage_bdb_jun": str(bd_perc_jun)+'%',

                

                
                #------jul22-------
                

                "recievable_jul": custom_data['recievable_jul'],
                "ondue_jul": custom_data['ondue_jul'],
                "afterdue_jul": custom_data['afterdue_jul'],
                "firstmon_jul":custom_data['firstmon_jul'],
                "secmon_jul":custom_data['secmon_jul'],
                "thirdmon_jul": custom_data['thirdmon_jul'],
                "actual_recievable_jul":custom_data['actual_recievable_jul'],
                "total_recieve_jul":tr_jul,
                "bad_debt_jul": bd_jul,
                "percentage_bdb_jul": str(bd_perc_jul)+'%',

                

                
                #------aug22-------
                

                "recievable_aug": custom_data['recievable_aug'],
                "ondue_aug": custom_data['ondue_aug'],
                "afterdue_aug": custom_data['afterdue_aug'],
                "firstmon_aug":custom_data['firstmon_aug'],
                "secmon_aug":custom_data['secmon_aug'],
                "thirdmon_aug": custom_data['thirdmon_aug'],
                "actual_recievable_aug":custom_data['actual_recievable_aug'],
                "total_recieve_aug":tr_aug,
                "bad_debt_aug": bd_aug,
                "percentage_bdb_aug": str(bd_perc_aug)+'%',

                
                
                #------sep22-------
                

                "recievable_sep": custom_data['recievable_sep'],
                "ondue_sep": custom_data['ondue_sep'],
                "afterdue_sep": custom_data['afterdue_sep'],
                "firstmon_sep":custom_data['firstmon_sep'],
                "secmon_sep":custom_data['secmon_sep'],
                "thirdmon_sep": custom_data['thirdmon_sep'],
                "actual_recievable_sep":custom_data['actual_recievable_sep'],
                "total_recieve_sep":tr_sep,
                "bad_debt_sep": bd_sep,
                "percentage_bdb_sep": str(bd_perc_sep)+'%',

                
                
                #------oct22-------

                "recievable_oct": custom_data['recievable_oct'],
                "ondue_oct": custom_data['ondue_oct'],
                "afterdue_oct": custom_data['afterdue_oct'],
                "firstmon_oct":custom_data['firstmon_oct'],
                "secmon_oct":custom_data['secmon_oct'],
                "thirdmon_oct": custom_data['thirdmon_oct'],
                "actual_recievable_oct":custom_data['actual_recievable_oct'],
                "total_recieve_oct":tr_oct,
                "bad_debt_oct": bd_oct,
                "percentage_bdb_oct":str(bd_perc_oct)+'%',

                

                
                #------nov22-------

                "recievable_nov": custom_data['recievable_nov'],
                "ondue_nov": custom_data['ondue_nov'],
                "afterdue_nov": custom_data['afterdue_nov'],
                "firstmon_nov":custom_data['firstmon_nov'],
                "secmon_nov":custom_data['secmon_nov'],
                "thirdmon_nov": custom_data['thirdmon_nov'],
                "actual_recievable_nov":custom_data['actual_recievable_nov'],
                "total_recieve_nov":tr_nov,
                "bad_debt_nov": bd_nov,
                "percentage_bdb_nov": str(bd_perc_nov)+'%' ,

                

                
                #------dec22-------
                

                "recievable_dec": custom_data['recievable_dec'],
                "ondue_dec": custom_data['ondue_dec'],
                "afterdue_dec": custom_data['afterdue_dec'],
                "firstmon_dec":custom_data['firstmon_dec'],
                "secmon_dec":custom_data['secmon_dec'],
                "thirdmon_dec": custom_data['thirdmon_dec'],
                "actual_recievable_dec":custom_data['actual_recievable_dec'],
                "total_recieve_dec":tr_dec,
                "bad_debt_dec": bd_dec,
                "percentage_bdb_dec": str(bd_perc_dec)+'%',

                
                        #------jan23-------
                
                "recievable_jan_2":  custom_data['recievable_jan_2'],
                "ondue_jan_2": custom_data['ondue_jan_2'],
                "afterdue_jan_2": custom_data['afterdue_jan_2'],
                "firstmon_jan_2": custom_data['firstmon_jan_2'],
                "secmon_jan_2":custom_data['secmon_jan_2'],
                "thirdmon_jan_2": custom_data['thirdmon_jan_2'],
                "actual_recievable_jan_2":custom_data['actual_recievable_jan_2'],
                "total_recieve_jan_2":tr_jan_2,
                "bad_debt_jan_2":bd_jan_2,
                "percentage_bdb_jan_2": str(bd_perc_jan_2)+'%',

                
                #------feb23-------
                

                "recievable_feb_2": custom_data['recievable_feb_2'],
                "ondue_feb_2": custom_data['ondue_feb_2'],
                "afterdue_feb_2": custom_data['afterdue_feb_2'],
                "firstmon_feb_2":custom_data['firstmon_feb_2'],
                "secmon_feb_2":custom_data['secmon_feb_2'],
                "thirdmon_feb_2": custom_data['thirdmon_feb_2'],
                "actual_recievable_feb_2":custom_data['actual_recievable_feb_2'],
                "total_recieve_feb_2":tr_feb_2,
                "bad_debt_feb_2": bd_feb_2,
                "percentage_bdb_feb_2":str(bd_perc_feb_2)+'%',

                
                
                #------mar23-------
                

                "recievable_mar_2": custom_data['recievable_mar_2'],
                "ondue_mar_2": custom_data['ondue_mar_2'],
                "afterdue_mar_2": custom_data['afterdue_mar_2'],
                "firstmon_mar_2":custom_data['firstmon_mar_2'],
                "secmon_mar_2":custom_data['secmon_mar_2'],
                "thirdmon_mar_2": custom_data['thirdmon_mar_2'],
                "actual_recievable_mar_2":custom_data['actual_recievable_mar_2'],
                "total_recieve_mar_2":tr_mar_2,
                "bad_debt_mar_2": bd_mar_2,
                "percentage_bdb_mar_2": str(bd_perc_mar_2)+'%',

                

                
                #------apr23-------
                

                "recievable_apr_2": custom_data['recievable_apr_2'],
                "ondue_apr_2": custom_data['ondue_apr_2'],
                "afterdue_apr_2": custom_data['afterdue_apr_2'],
                "firstmon_apr_2":custom_data['firstmon_apr_2'],
                "secmon_apr_2":custom_data['secmon_apr_2'],
                "thirdmon_apr_2": custom_data['thirdmon_apr_2'],
                "actual_recievable_apr_2":custom_data['actual_recievable_apr_2'],
                "total_recieve_apr_2":tr_apr_2,
                "bad_debt_apr_2": bd_apr_2,
                "percentage_bdb_apr_2": str(bd_perc_apr_2)+'%',

                

                
                #------may23-------
                

                "recievable_may_2": custom_data['recievable_may_2'],
                "ondue_may_2": custom_data['ondue_may_2'],
                "afterdue_may_2": custom_data['afterdue_may_2'],
                "firstmon_may_2":custom_data['firstmon_may_2'],
                "secmon_may_2":custom_data['secmon_may_2'],
                "thirdmon_may_2": custom_data['thirdmon_may_2'],
                "actual_recievable_may_2":custom_data['actual_recievable_may_2'],
                "total_recieve_may_2":tr_may_2,
                "bad_debt_may_2": bd_may_2,
                "percentage_bdb_may_2": str(bd_perc_may_2)+'%',

                
                
                #------jun23-------
                

                "recievable_jun_2": custom_data['recievable_jun_2'],
                "ondue_jun_2": custom_data['ondue_jun_2'],
                "afterdue_jun_2": custom_data['afterdue_jun_2'],
                "firstmon_jun_2":custom_data['firstmon_jun_2'],
                "secmon_jun_2":custom_data['secmon_jun_2'],
                "thirdmon_jun_2": custom_data['thirdmon_jun_2'],
                "actual_recievable_jun_2":custom_data['actual_recievable_jun_2'],
                "total_recieve_jun_2":tr_jun_2,
                "bad_debt_jun_2": bd_jun_2,
                "percentage_bdb_jun_2": str(bd_perc_jun_2)+'%',

                

                
                #------jul23-------
                

                "recievable_jul_2": custom_data['recievable_jul_2'],
                "ondue_jul_2": custom_data['ondue_jul_2'],
                "afterdue_jul_2": custom_data['afterdue_jul_2'],
                "firstmon_jul_2":custom_data['firstmon_jul_2'],
                "secmon_jul_2":custom_data['secmon_jul_2'],
                "thirdmon_jul_2": custom_data['thirdmon_jul_2'],
                "actual_recievable_jul_2":custom_data['actual_recievable_jul_2'],
                "total_recieve_jul_2":tr_jul_2,
                "bad_debt_jul_2": bd_jul_2,
                "percentage_bdb_jul_2": str(bd_perc_jul_2)+'%',

                

                
                #------aug23-------
                

                "recievable_aug_2": custom_data['recievable_aug_2'],
                "ondue_aug_2": custom_data['ondue_aug_2'],
                "afterdue_aug_2": custom_data['afterdue_aug_2'],
                "firstmon_aug_2":custom_data['firstmon_aug_2'],
                "secmon_aug_2":custom_data['secmon_aug_2'],
                "thirdmon_aug_2": custom_data['thirdmon_aug_2'],
                "actual_recievable_aug_2":custom_data['actual_recievable_aug_2'],
                "total_recieve_aug_2":tr_aug_2,
                "bad_debt_aug_2": bd_aug_2,
                "percentage_bdb_aug_2": str(bd_perc_aug_2)+'%',

                

                
                #------sep23-------
                

                "recievable_sep_2": custom_data['recievable_sep_2'],
                "ondue_sep_2": custom_data['ondue_sep_2'],
                "afterdue_sep_2": custom_data['afterdue_sep_2'],
                "firstmon_sep_2":custom_data['firstmon_sep_2'],
                "secmon_sep_2":custom_data['secmon_sep_2'],
                "thirdmon_sep_2": custom_data['thirdmon_sep_2'],
                "actual_recievable_sep_2":custom_data['actual_recievable_sep_2'],
                "total_recieve_sep_2":tr_sep_2,
                "bad_debt_sep_2": bd_sep_2,
                "percentage_bdb_sep_2":str(bd_perc_sep_2)+'%',

                
                
                #------oct23-------

                "recievable_oct_2": custom_data['recievable_oct_2'],
                "ondue_oct_2": custom_data['ondue_oct_2'],
                "afterdue_oct_2": custom_data['afterdue_oct_2'],
                "firstmon_oct_2":custom_data['firstmon_oct_2'],
                "secmon_oct_2":custom_data['secmon_oct_2'],
                "thirdmon_oct_2": custom_data['thirdmon_oct_2'],
                "actual_recievable_oct_2":custom_data['actual_recievable_oct_2'],
                "total_recieve_oct_2":tr_oct_2,
                "bad_debt_oct_2": bd_oct_2,
                "percentage_bdb_oct_2": str(bd_perc_oct_2)+'%',

                
                
                #------nov23-------
                

                "recievable_nov_2": custom_data['recievable_nov_2'],
                "ondue_nov_2": custom_data['ondue_nov_2'],
                "afterdue_nov_2": custom_data['afterdue_nov_2'],
                "firstmon_nov_2":custom_data['firstmon_nov_2'],
                "secmon_nov_2":custom_data['secmon_nov_2'],
                "thirdmon_nov_2": custom_data['thirdmon_nov_2'],
                "actual_recievable_nov_2":custom_data['actual_recievable_nov_2'],
                "total_recieve_nov_2":tr_nov_2,
                "bad_debt_nov_2": bd_nov_2,
                "percentage_bdb_nov_2": str(bd_perc_nov_2)+'%',

                
                
                #------dec23-------
                

                "recievable_dec_2": custom_data['recievable_dec_2'],
                "ondue_dec_2": custom_data['ondue_dec_2'],
                "afterdue_dec_2": custom_data['afterdue_dec_2'],
                "firstmon_dec_2":custom_data['firstmon_dec_2'],
                "secmon_dec_2":custom_data['secmon_dec_2'],
                "thirdmon_dec_2": custom_data['thirdmon_dec_2'],
                "actual_recievable_dec_2":custom_data['actual_recievable_dec_2'],
                "total_recieve_dec_2":tr_dec_2,
                "bad_debt_dec_2": bd_dec_2,
                "percentage_bdb_dec_2": str(bd_perc_dec_2)+'%',

                
                
    
            })
            lines.append(mvl.id)
            lst=[]
            lst.append(mvl['student_branch'])
            lst.append(mvl['student_campus'])
            lst.append(mvl['recievable_jan_2'])
            lst.append(mvl['ondue_jan_2'])
            lst.append(mvl['afterdue_jan_2'])
            lst.append(mvl['firstmon_jan_2'])
            lst.append(mvl['secmon_jan_2'])
            lst.append(mvl['thirdmon_jan_2'])
            lst.append(mvl['thirdmon_jan_2'])
            lst.append(mvl['actual_recievable_jan_2'])
            lst.append(mvl['bad_debt_jan_2'])
            _logger.info(f"branch: {lst}")


            
            
            
            
            self.write({
                "account_report_line":[(6,0,lines)]
            }

            )
            # raise UserError(str(final_lst))
        
       
        

        
            
    
    def action_print_excel_report(self):
        

        self.action_print_report()
        
        
        if xlwt:

            
            filename = 'Aging Report.xls'
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('agings of Withdrawl Std')
            

            
            style_title = xlwt.easyxf(
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            red_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour tan;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            yellow_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            lime_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour aqua;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")

            grand_heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;'
                              'font: colour black, bold True;')

            heading_style = xlwt.easyxf('align: vertical center,horiz center;')
            
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'dd/mm/yyyy'

            # worksheet.write_merge(0, 1, 0, 5,"LACAS SCHOOL NETWORK ",style=style_title)
            # worksheet.write_merge(0, 1, 6, 11, "aging Report OF  STUDENTS", style=style_title)
            
            

            worksheet.write_merge(0,1,0,0,"Sr.No", style=red_style_title)
            worksheet.write_merge(0,1,1,1,"Campus",style=red_style_title)
            worksheet.write_merge(0,1,2,2,"Branch Name",style=red_style_title)



            v_from_month=datetime.strptime(str(self.date_from), "%Y-%m-%d").strftime('%m')
            v_from_year=datetime.strptime(str(self.date_from), "%Y-%m-%d").strftime('%y')

            v_to_month=datetime.strptime(str(self.date_to), "%Y-%m-%d").strftime('%m')
            v_to_year=datetime.strptime(str(self.date_to), "%Y-%m-%d").strftime('%y')

            months= {
                1:['01','JAN-22 (RECEIVABLES)','JAN-22 (ON DUE)','JAN-22 (AFTER DUE ON JAN)','JAN-22 (30 DAYS)','JAN-22 (60 DAYS)','JAN-22 (90 DAYS)',
                'JAN-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',10,'22'],
                2:['02','FEB-22 (RECEIVABLES)','FEB-22 (ON DUE)','FEB-22 (AFTER DUE ON JAN)','FEB-22 (30 DAYS)','FEB-22 (60 DAYS)','FEB-22 (90 DAYS)',
                'FEB-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',20,'22'],
                3:['03','MAR-22 (RECEIVABLES)','MAR-22 (ON DUE)','MAR-22 (AFTER DUE ON JAN)','MAR-22 (30 DAYS)','MAR-22 (60 DAYS)','MAR-22 (90 DAYS)',
                'MAR-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',30,'22'],
                4:['04','APR-22 (RECEIVABLES)','APR-22 (ON DUE)','APR-22 (AFTER DUE ON JAN)','APR-22 (30 DAYS)','APR-22 (60 DAYS)','APR-22 (90 DAYS)',
                'APR-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',40,'22'],
                5:['05','MAY-22 (RECEIVABLES)','MAY-22 (ON DUE)','MAY-22 (AFTER DUE ON JAN)','MAY-22 (30 DAYS)','MAY-22 (60 DAYS)','MAY-22 (90 DAYS)',
                'MAY-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',50,'22'],
                6:['06','JUN-22 (RECEIVABLES)','JUN-22 (ON DUE)','JUN-22 (AFTER DUE ON JAN)','JUN-22 (30 DAYS)','JUN-22 (60 DAYS)','JUN-22 (90 DAYS)',
                'JUN-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',60,'22'],
                7:['07','JUL-22 (RECEIVABLES)','JUL-22 (ON DUE)','JUL-22 (AFTER DUE ON JAN)','JUL-22 (30 DAYS)','JUL-22 (60 DAYS)','JUL-22 (90 DAYS)',
                'JUL-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',70,'22'],
                8:['08','AUG-22 (RECEIVABLES)','AUG-22 (ON DUE)','AUG-22 (AFTER DUE ON JAN)','AUG-22 (30 DAYS)','AUG-22 (60 DAYS)','AUG-22 (90 DAYS)',
                'AUG-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',80,'22'],
                9:['09','SEP-22 (RECEIVABLES)','SEP-22 (ON DUE)','SEP-22 (AFTER DUE ON JAN)','SEP-22 (30 DAYS)','SEP-22 (60 DAYS)','SEP-22 (90 DAYS)',
                'SEP-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',90,'22'],
                10:['10','OCT-22 (RECEIVABLES)','OCT-22 (ON DUE)','OCT-22 (AFTER DUE ON JAN)','OCT-22 (30 DAYS)','OCT-22 (60 DAYS)','OCT-22 (90 DAYS)',
                'OCT-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',100,'22'],
                11:['11','NOV-22 (RECEIVABLES)','NOV-22 (ON DUE)','NOV-22 (AFTER DUE ON JAN)','NOV-22 (30 DAYS)','NOV-22 (60 DAYS)','NOV-22 (90 DAYS)',
                'NOV-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',110,'22'],
                12:['12','DEC-22 (RECEIVABLES)','DEC-22 (ON DUE)','DEC-22 (AFTER DUE ON JAN)','DEC-22 (30 DAYS)','DEC-22 (60 DAYS)','DEC-22 (90 DAYS)',
                'DEC-22 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',120,'22'],
                13:['01','JAN-23 (RECEIVABLES)','JAN-23 (ON DUE)','JAN-23 (AFTER DUE ON JAN)','JAN-23 (30 DAYS)','JAN-23 (60 DAYS)','JAN-23 (90 DAYS)',
                'JAN-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',130,'23'],
                14:['02','FEB-23 (RECEIVABLES)','FEB-23 (ON DUE)','FEB-23 (AFTER DUE ON FEB)','FEB-23 (30 DAYS)','FEB-23 (60 DAYS)','FEB-23 (90 DAYS)',
                'FEB-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',140,'23'],
                15:['03','MAR-23 (RECEIVABLES)','MAR-23 (ON DUE)','MAR-23 (AFTER DUE ON MAR)','MAR-23 (30 DAYS)','MAR-23 (60 DAYS)','MAR-23 (90 DAYS)',
                'MAR-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',150,'23'],
                16:['04','APR-23 (RECEIVABLES)','APR-23 (ON DUE)','APR-23 (AFTER DUE ON APR)','APR-23 (30 DAYS)','APR-23 (60 DAYS)','APR-23 (90 DAYS)',
                'APR-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',160,'23'],
                17:['05','MAY-23 (RECEIVABLES)','MAY-23 (ON DUE)','MAY-23 (AFTER DUE ON MAY)','MAY-23 (30 DAYS)','MAY-23 (60 DAYS)','MAY-23 (90 DAYS)',
                'MAY-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',170,'23'],
                18:['06','JUN-23 (RECEIVABLES)','JUN-23 (ON DUE)','JUN-23 (AFTER DUE ON JUN)','JUN-23 (30 DAYS)','JUN-23 (60 DAYS)','JUN-23 (90 DAYS)',
                'JUN-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',180,'23'],
                19:['07','JUL-23 (RECEIVABLES)','JUL-23 (ON DUE)','JUL-23 (AFTER DUE ON JUL)','JUL-23 (30 DAYS)','JUL-23 (60 DAYS)','JUL-23 (90 DAYS)',
                'JUL-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',190,'23'],
                20:['08','AUG-23 (RECEIVABLES)','AUG-23 (ON DUE)','AUG-23 (AFTER DUE ON AUG)','AUG-23 (30 DAYS)','AUG-23 (60 DAYS)','AUG-23 (90 DAYS)',
                'AUG-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',200,'23'],
                21:['09','SEP-23 (RECEIVABLES)','SEP-23 (ON DUE)','SEP-23 (AFTER DUE ON SEP)','SEP-23 (30 DAYS)','SEP-23 (60 DAYS)','SEP-23 (90 DAYS)',
                'SEP-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',200,'23'],
                22:['10','OCT-23 (RECEIVABLES)','OCT-23 (ON DUE)','OCT-23 (AFTER DUE ON OCT)','OCT-23 (30 DAYS)','OCT-23 (60 DAYS)','OCT-23 (90 DAYS)',
                'OCT-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',200,'23'],
                23:['11','NOV-23 (RECEIVABLES)','NOV-23 (ON DUE)','NOV-23 (AFTER DUE ON NOV)','NOV-23 (30 DAYS)','NOV-23 (60 DAYS)','NOV-23 (90 DAYS)',
                'NOV-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',200,'23'],
                24:['12','DEC-23 (RECEIVABLES)','DEC-23 (ON DUE)','DEC-23 (AFTER DUE ON DEC)','DEC-23 (30 DAYS)','DEC-23 (60 DAYS)','DEC-23 (90 DAYS)',
                'DEC-23 (Recovery after 90 days)','Total Received and Receivables','Bade Debts','Percentage of Bad Debts',200,'23'],
                }
            range_start = 0
            range_stop = 0
            # raise UserError(v_to)
            for key, value in months.items():
                if value[0] == v_from_month and value[12] == v_from_year:
                    range_start = key
                if value[0] == v_to_month and value[12] == v_to_year:

                    range_stop = key

            col = 3
            
      
            for i in range(range_start,range_stop+1):
      
                worksheet.write_merge(0,1,col,col,months[i][1],lime_style_title)
                worksheet.write_merge(0,1,col+1,col+1,months[i][2],lime_style_title)
                worksheet.write_merge(0,1,col+2,col+2,months[i][3],lime_style_title)
                worksheet.write_merge(0,1,col+3,col+3,months[i][4],lime_style_title)
                worksheet.write_merge(0,1,col+4,col+4,months[i][5],lime_style_title)
                worksheet.write_merge(0,1,col+5,col+5,months[i][6],lime_style_title)
                worksheet.write_merge(0,1,col+6,col+6,months[i][7],lime_style_title)
                worksheet.write_merge(0,1,col+7,col+7,months[i][8],lime_style_title)
                worksheet.write_merge(0,1,col+8,col+8,months[i][9],lime_style_title)
                worksheet.write_merge(0,1,col+9,col+9,months[i][10],lime_style_title)

            
                col+=10

        #     worksheet.write_merge(0,1,col,col+1,"Total", lime_style_title)   
            
        #         # print('col:',months[i][1], 'data:',months[i][2])

            column = 3
            row = 2
            sn=1
            for rec in self.account_report_line:
                if rec:

                    column = 3

                    worksheet.write(row,0,sn)
                    worksheet.write_merge(row,row,1,1,rec.student_campus,heading_style)
                    worksheet.write_merge(row,row,2,2,rec.student_branch,heading_style)

  

                    data_month= {
                        1:['01','JAN-22',rec.recievable_jan,rec.ondue_jan,rec.afterdue_jan,rec.firstmon_jan,rec.secmon_jan,
                        rec.thirdmon_jan,rec.actual_recievable_jan,rec.total_recieve_jan,rec.bad_debt_jan,rec.percentage_bdb_jan,'22'],

                        2:['02','FEB-22',rec.recievable_feb,rec.ondue_feb,rec.afterdue_feb,rec.firstmon_feb,rec.secmon_feb,
                        rec.thirdmon_feb,rec.actual_recievable_feb,rec.total_recieve_feb,rec.bad_debt_feb,rec.percentage_bdb_feb,'22'],

                        3:['03','MAR-22',rec.recievable_mar,rec.ondue_mar,rec.afterdue_mar,rec.firstmon_mar,rec.secmon_mar,
                        rec.thirdmon_mar,rec.actual_recievable_mar,rec.total_recieve_mar,rec.bad_debt_mar,rec.percentage_bdb_mar,'22'],

                        4:['04','APR-22',rec.recievable_apr,rec.ondue_apr,rec.afterdue_apr,rec.firstmon_apr,rec.secmon_apr,
                        rec.thirdmon_apr,rec.actual_recievable_apr,rec.total_recieve_apr,rec.bad_debt_apr,rec.percentage_bdb_apr,'22'],

                        5:['05','MAY-22',rec.recievable_may,rec.ondue_may,rec.afterdue_may,rec.firstmon_may,rec.secmon_may,
                        rec.thirdmon_may,rec.actual_recievable_may,rec.total_recieve_may,rec.bad_debt_may,rec.percentage_bdb_may,'22'],

                        6:['06','JUN-22',rec.recievable_jun,rec.ondue_jun,rec.afterdue_jun,rec.firstmon_jun,rec.secmon_jun,
                        rec.thirdmon_jun,rec.actual_recievable_jun,rec.total_recieve_jun,rec.bad_debt_jun,rec.percentage_bdb_jun,'22'],

                        7:['07','JUL-22',rec.recievable_jul,rec.ondue_jul,rec.afterdue_jul,rec.firstmon_jul,rec.secmon_jul,
                        rec.thirdmon_jul,rec.actual_recievable_jul,rec.total_recieve_jul,rec.bad_debt_jul,rec.percentage_bdb_jul,'22'],

                        8:['08','AUG-22',rec.recievable_aug,rec.ondue_aug,rec.afterdue_aug,rec.firstmon_aug,rec.secmon_aug,
                        rec.thirdmon_aug,rec.actual_recievable_aug,rec.total_recieve_aug,rec.bad_debt_aug,rec.percentage_bdb_aug,'22'],

                        9:['09','SEP-22',rec.recievable_sep,rec.ondue_sep,rec.afterdue_sep,rec.firstmon_sep,rec.secmon_sep,
                        rec.thirdmon_sep,rec.actual_recievable_sep,rec.total_recieve_sep,rec.bad_debt_sep,rec.percentage_bdb_sep,'22'],

                        10:['10','OCT-22',rec.recievable_oct,rec.ondue_oct,rec.afterdue_oct,rec.firstmon_oct,rec.secmon_oct,
                        rec.thirdmon_oct,rec.actual_recievable_oct,rec.total_recieve_oct,rec.bad_debt_oct,rec.percentage_bdb_oct,'22'],

                        11:['11','NOV-22',rec.recievable_nov,rec.ondue_nov,rec.afterdue_nov,rec.firstmon_nov,rec.secmon_nov,
                        rec.thirdmon_nov,rec.actual_recievable_nov,rec.total_recieve_nov,rec.bad_debt_nov,rec.percentage_bdb_nov,'22'],

                        12:['12','DEC-22',rec.recievable_dec,rec.ondue_dec,rec.afterdue_dec,rec.firstmon_dec,rec.secmon_dec,
                        rec.thirdmon_dec,rec.actual_recievable_dec,rec.total_recieve_dec,rec.bad_debt_dec,rec.percentage_bdb_dec,'22'],

                        13:['01','JAN-23',rec.recievable_jan_2,rec.ondue_jan_2,rec.afterdue_jan_2,rec.firstmon_jan_2,rec.secmon_jan_2,
                        rec.thirdmon_jan_2,rec.actual_recievable_jan_2,rec.total_recieve_jan_2,rec.bad_debt_jan_2,rec.percentage_bdb_jan_2,'23'],

                        14:['02','FEB-23',rec.recievable_feb_2,rec.ondue_feb_2,rec.afterdue_feb_2,rec.firstmon_feb_2,rec.secmon_feb_2,
                        rec.thirdmon_feb_2,rec.actual_recievable_feb_2,rec.total_recieve_feb_2,rec.bad_debt_feb_2,rec.percentage_bdb_feb_2,'23'],

                        15:['03','MAR-23',rec.recievable_mar_2,rec.ondue_mar_2,rec.afterdue_mar_2,rec.firstmon_mar_2,rec.secmon_mar_2,
                        rec.thirdmon_mar_2,rec.actual_recievable_mar_2,rec.total_recieve_mar_2,rec.bad_debt_mar_2,rec.percentage_bdb_mar_2,'23'],

                        16:['04','APR-23',rec.recievable_apr_2,rec.ondue_apr_2,rec.afterdue_apr_2,rec.firstmon_apr_2,rec.secmon_apr_2,
                        rec.thirdmon_apr_2,rec.actual_recievable_apr_2,rec.total_recieve_apr_2,rec.bad_debt_apr_2,rec.percentage_bdb_apr_2,'23'],

                        17:['05','MAY-23',rec.recievable_may_2,rec.ondue_may_2,rec.afterdue_may_2,rec.firstmon_may_2,rec.secmon_may_2,
                        rec.thirdmon_may_2,rec.actual_recievable_may_2,rec.total_recieve_may_2,rec.bad_debt_may_2,rec.percentage_bdb_may_2,'23'],

                        18:['06','JUN-23',rec.recievable_may_2,rec.ondue_may_2,rec.afterdue_may_2,rec.firstmon_may_2,rec.secmon_may_2,
                        rec.thirdmon_may_2,rec.actual_recievable_may_2,rec.total_recieve_may_2,rec.bad_debt_may_2,rec.percentage_bdb_may_2,'23'],

                        19:['07','JUL-23',rec.recievable_jul_2,rec.ondue_jul_2,rec.afterdue_jul_2,rec.firstmon_jul_2,rec.secmon_jul_2,
                        rec.thirdmon_jul_2,rec.actual_recievable_jul_2,rec.total_recieve_jul_2,rec.bad_debt_jul_2,rec.percentage_bdb_jul_2,'23'],

                        20:['08','AUG-23',rec.recievable_aug_2,rec.ondue_aug_2,rec.afterdue_aug_2,rec.firstmon_aug_2,rec.secmon_aug_2,
                        rec.thirdmon_aug_2,rec.actual_recievable_aug_2,rec.total_recieve_aug_2,rec.bad_debt_aug_2,rec.percentage_bdb_aug_2,'23'],

                        21:['09','SEP-23',rec.recievable_sep_2,rec.ondue_sep_2,rec.afterdue_sep_2,rec.firstmon_sep_2,rec.secmon_sep_2,
                        rec.thirdmon_sep_2,rec.actual_recievable_sep_2,rec.total_recieve_sep_2,rec.bad_debt_sep_2,rec.percentage_bdb_sep_2,'23'],

                        22:['10','OCT-23',rec.recievable_oct_2,rec.ondue_oct_2,rec.afterdue_oct_2,rec.firstmon_oct_2,rec.secmon_oct_2,
                        rec.thirdmon_oct_2,rec.actual_recievable_oct_2,rec.total_recieve_oct_2,rec.bad_debt_oct_2,rec.percentage_bdb_oct_2,'23'],

                        23:['11','NOV-23',rec.recievable_nov_2,rec.ondue_nov_2,rec.afterdue_nov_2,rec.firstmon_nov_2,rec.secmon_nov_2,
                        rec.thirdmon_nov_2,rec.actual_recievable_nov_2,rec.total_recieve_nov_2,rec.bad_debt_nov_2,rec.percentage_bdb_nov_2,'23'],

                        24:['12','DEC-23',rec.recievable_dec_2,rec.ondue_dec_2,rec.afterdue_dec_2,rec.firstmon_dec_2,rec.secmon_dec_2,
                        rec.thirdmon_dec_2,rec.actual_recievable_dec_2,rec.total_recieve_dec_2,rec.bad_debt_dec_2,rec.percentage_bdb_dec_2,'23'],

                    }
                    range_start = 0
                    range_stop = 0
                  
                    for key, value in data_month.items():
                        if value[0] == v_from_month and value[12] == v_from_year:
                            range_start = key
                        if value[0] == v_to_month and value[12] == v_to_year:
                            range_stop = key
                    

                    for i in range(range_start,range_stop+1):
                        # raise UserError(column)
                        worksheet.write_merge(row,row,column,column,data_month[i][2],heading_style)
                        worksheet.write_merge(row,row,column+1,column+1,data_month[i][3],heading_style)
                        worksheet.write_merge(row,row,column+2,column+2,data_month[i][4],heading_style)
                        worksheet.write_merge(row,row,column+3,column+3,data_month[i][5],heading_style)
                        worksheet.write_merge(row,row,column+4,column+4,data_month[i][6],heading_style)
                        worksheet.write_merge(row,row,column+5,column+5,data_month[i][7],heading_style)
                        worksheet.write_merge(row,row,column+6,column+6,data_month[i][8],heading_style)
                        worksheet.write_merge(row,row,column+7,column+7,data_month[i][9],heading_style)
                        worksheet.write_merge(row,row,column+8,column+8,data_month[i][10],heading_style)
                        worksheet.write_merge(row,row,column+9,column+9,data_month[i][11],heading_style)

                        # worksheet.write_merge(row,row,column,column+1,rec.total_amount)
                        # lst.append([row_1,row_1,column,column+1])
                      
                        column+=10
                    # worksheet.write_merge(row,row,column,column+1,rec.total_amount,heading_style)
                      
                    row+=1
                    sn+=1

            fp = io.BytesIO()
            workbook.save(fp)

            export_id = self.env['sale.day.book.report.excel'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
            res = {
                    'view_mode': 'form',
                    'res_id': export_id.id,
                    'res_model': 'sale.day.book.report.excel',
                    'type': 'ir.actions.act_window',
                    'target':'new'
                }
            return res
            
        else:
            raise Warning (""" You Don't have xlwt library.\n Please install it by executing this command :  sudo pip3 install xlwt""")
        

   
                

           

























