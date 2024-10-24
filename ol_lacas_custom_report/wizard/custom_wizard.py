
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
import xlsxwriter
from xlwt import easyxf
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
    _name = 'account.report.move.line'
    
    record_id=fields.Char('ID')
    roll_no=fields.Integer('Roll No')
    full_roll_no=fields.Integer('Roll No')
    full_roll_number=fields.Integer('Roll No')
    student_batch=fields.Char('Batch')
    student_branch=fields.Char('Branch')
    student_class=fields.Char('Class')
    withdrawn_status=fields.Char('Withdrawn Status')
    leaving_reason=fields.Char('Leaving Reason')
    remarks=fields.Char('Remarks')
    withdrawn_date=fields.Char('Withdrawn Date')
    app_date=fields.Char('Withdrawn Date')
    total_amount=fields.Float("Total")
    name=fields.Char('Name')
    jan=fields.Integer('JAN-22')
    feb=fields.Integer('FEB-22')
    mar=fields.Integer('MAR-22')
    apr=fields.Integer('APR-22')
    may=fields.Integer('MAY-22')
    jun=fields.Integer('JUN-22')
    jul=fields.Integer('JUL-22')
    aug=fields.Integer('AUG-22')
    sep=fields.Integer('SEP-22')
    oct=fields.Integer('OCT-22')
    nov=fields.Integer('NOV-22')
    dec=fields.Integer('DEC-22')
    
    jan_2=fields.Integer('JAN-23')
    feb_2=fields.Integer('FEB-23')
    mar_2=fields.Integer('MAR-23')
    apr_2=fields.Integer('APR-23')
    may_2=fields.Integer('MAY-23')
    jun_2=fields.Integer('JUN-23')
    jul_2=fields.Integer('JUL-23')
    aug_2=fields.Integer('AUG-23')
    sep_2=fields.Integer('SEP-23')
    oct_2=fields.Integer('OCT-23')
    nov_2=fields.Integer('NOV-23')
    dec_2=fields.Integer('DEC-23')

    jan_3=fields.Integer('JAN-24')
    feb_3=fields.Integer('FEB-24')
    mar_3=fields.Integer('MAR-24')
    apr_3=fields.Integer('APR-24')
    may_3=fields.Integer('MAY-24')
    jun_3=fields.Integer('JUN-24')
    jul_3=fields.Integer('JUL-24')
    aug_3=fields.Integer('AUG-24')
    sep_3=fields.Integer('SEP-24')
    oct_3=fields.Integer('OCT-24')
    nov_3=fields.Integer('NOV-24')
    dec_3=fields.Integer('DEC-24')

  

    
   

class ReceivablesReportWizard(models.TransientModel):
    _name="receivable.report.wizard"
    _description='Print receivable Wizard'

    date_from=fields.Date(string="Date From")
    date_to=fields.Date(string="Date To")
    std_type=fields.Selection([('enrolled','Enrolled Student'),('graduated','Graduated')],string="Student Category")

    account_report_line=fields.Many2many('account.report.move.line', string='Account report Line')
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

                if  from_year < '22' or from_year >'24':
                    raise UserError("Sorry, Year must be between 2022-2024..")
                    raise ValidationError(_('Sorry, Year must be 2022-2024...'))

                elif to_year <"22" or to_year >"24":
                    raise UserError("Sorry, Year must be between 2022-2024..")
                    raise ValidationError(_('Sorry, Year must be 2022-2024...'))

        


    


  
    
    def action_print_report(self):
    
        global first_date
        global last_date

        domain = [
            ('move_type', '=', 'out_refund'),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            ('journal_id.name', '!=', 'Admission Challan'),
           
        ]

        if self.std_type == 'enrolled':
            domain.append(('x_student_id_cred.x_last_enrollment_status_id.name', '=', 'Enrolled'))
        elif self.std_type == 'graduated':
            domain.append(('x_student_id_cred.x_last_enrollment_status_id.name', '=', 'Graduated'))

        move_ids_raw = self.env['account.move'].search(domain)

        # raise UserError(domain)

        std_lst = []
        for rec in move_ids_raw:
            if len(rec.unpaid_std_inv_ids) > 0:
                for line in rec.unpaid_std_inv_ids:
                    if line.state == 'posted':
                        std_lst.append(rec.x_student_id_cred.id)

        domain_2 = [
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
            ('payment_state', 'in', ['not_paid', 'partial']),
            ('student_ids', 'in', std_lst),
        ]

        inv_ids = self.env['account.move'].search(domain_2)
        sorted_inv_ids = sorted(inv_ids, key=lambda inv: inv.invoice_date.strftime("%Y-%m"))

        if sorted_inv_ids:
            first_date = sorted_inv_ids[0].invoice_date
            last_date = sorted_inv_ids[-1].invoice_date
        else:
            raise UserError(str("There are no receivables for the date from {} to {}").format(self.date_from, self.date_to))

            
            
                
        
        
        
        invoice_check = []
        final_lst = []
        temp_lst = []

        a=""
       
        for value in move_ids_raw:

            

            custom_data = {
                        "record_id":'',
                        "roll_no":0,
                        "name":'',
                        "full_roll_number":" ",
                        "student_batch":'',
                        "student_branch":"",
                        "student_class":'',
                        "withdrawn_status":"",
                        "leaving_reason":"",
                        "remarks":"",
                        "withdrawn_date":'',
                        "app_date":'',
                        "jan": 0,
                        "feb": 0,
                        "mar": 0,
                        "apr":0,
                        "may":0,
                        "jun": 0,
                        "jul":0,
                        "aug":0,
                        "sep": 0,
                        "oct": 0,
                        "nov": 0,
                        "dec": 0,

                        "jan_2": 0,
                        "feb_2": 0,
                        "mar_2": 0,
                        "apr_2":0,
                        "may_2":0,
                        "jun_2": 0,
                        "jul_2":0,
                        "aug_2":0,
                        "sep_2": 0,
                        "oct_2": 0,
                        "nov_2": 0,
                        "dec_2": 0,

                        "jan_3": 0,
                        "feb_3": 0,
                        "mar_3": 0,
                        "apr_3": 0,
                        "may_3": 0,
                        "jun_3": 0,
                        "jul_3": 0,
                        "aug_3": 0,
                        "sep_3": 0,
                        "oct_3": 0,
                        "nov_3": 0,
                        "dec_3": 0,
                        "total_amount":0
                    }
           

            custom_data['name'] = value.x_student_id_cred.name if value.x_student_id_cred.name else ''
            custom_data['record_id'] = value.name 
            custom_data['roll_no'] = value.x_student_id_cred.olf_id if value.x_student_id_cred.olf_id else 0
            custom_data['full_roll_number'] = value.x_student_id_cred.olf_udid if value.x_student_id_cred.olf_udid else 0
            custom_data['student_batch'] = value.x_studio_batch.x_name if value.x_studio_batch.x_name else ''
            # custom_data['student_branch'] = value.x_student_id_cred.school_ids.name if  value.x_student_id_cred.school_ids.name else ""
            if value.x_student_id_cred:
                if len(value.x_student_id_cred.school_ids)==1:
                    custom_data['student_branch'] = value.x_student_id_cred.school_ids.name
            custom_data['student_class'] = value.x_student_id_cred.homeroom if value.x_student_id_cred.homeroom else ''
            custom_data['withdrawn_status'] = value.x_studio_withdrawn_status
            custom_data['leaving_reason'] = value.leaving_reason.name if value.leaving_reason.name else ''
            custom_data['remarks'] = value.remarks if  value.remarks else ''
            custom_data['withdrawn_date'] = value.invoice_date 
            custom_data['app_date'] = value.withdrawl_submission_date if  value.withdrawl_submission_date  else ''

            # custom_data['name'] = value.partner_id.name
            # custom_data['record_id'] = value.name 
            # custom_data['roll_no'] =  0
            # custom_data['full_roll_number'] = 0
            # custom_data['student_batch'] =  ''
            # custom_data['student_branch'] =  ""
            # custom_data['student_class'] = ''
            # custom_data['withdrawn_status'] =  ''
            # custom_data['leaving_reason'] =  ''
            # custom_data['remarks'] = ''
            # custom_data['withdrawn_date'] = value.invoice_date
            # custom_data['app_date'] = value.x_studio_app_date if  value.x_studio_app_date  else ''


            
        
            if value.month_date == "January" and value.year_date=='22':
                custom_data['jan'] = value.amount_residual
            elif value.month_date == "Feburary" and value.year_date=='22':
                custom_data['feb'] = value.amount_residual
            elif value.month_date == "March"and value.year_date=='22':
                custom_data['mar'] = value.amount_residual
            elif value.month_date == "April" and value.year_date=='22':
                custom_data['apr'] = value.amount_residual
            elif value.month_date == "May" and value.year_date=='22':
                custom_data['may'] = value.amount_residual
            elif value.month_date == "June" and value.year_date=='22':
                custom_data['jun'] = value.amount_residual
            elif value.month_date == "July" and value.year_date=='22':
                custom_data['jul'] = value.amount_residual
            elif value.month_date == "August" and value.year_date=='22':
                custom_data['aug'] = value.amount_residual
            elif value.month_date == "September" and value.year_date=='22':
                custom_data['sep'] = value.amount_residual
            elif value.month_date == "October" and value.year_date=='22':
                custom_data['oct'] = value.amount_residual
            elif value.month_date == "November" and value.year_date=='22':
                custom_data['nov'] = value.amount_residual
            elif value.month_date == "December" and value.year_date=='22':
                custom_data['dec'] = value.amount_residual

            elif value.month_date == "January" and value.year_date=='23':
                custom_data['jan_2'] = value.amount_residual
            elif value.month_date == "Feburary" and value.year_date=='23':
                custom_data['feb_2'] = value.amount_residual
            elif value.month_date == "March"and value.year_date=='23':
                custom_data['mar_2'] = value.amount_residual
            elif value.month_date == "April" and value.year_date=='23':
                custom_data['apr_2'] = value.amount_residual
            elif value.month_date == "May" and value.year_date=='23':
                custom_data['may_2'] = value.amount_residual
            elif value.month_date == "June" and value.year_date=='23':
                custom_data['jun_2'] = value.amount_residual
            elif value.month_date == "July" and value.year_date=='23':
                custom_data['jul_2'] = value.amount_residual
            elif value.month_date == "August" and value.year_date=='23':
                custom_data['aug_2'] = value.amount_residual
            elif value.month_date == "September" and value.year_date=='23':
                custom_data['sep_2'] = value.amount_residual
            elif value.month_date == "October" and value.year_date=='23':
                custom_data['oct_2'] = value.amount_residual
            elif value.month_date == "November" and value.year_date=='23':
                custom_data['nov_2'] = value.amount_residual
            elif value.month_date == "December" and value.year_date=='23':
                custom_data['dec_2'] = value.amount_residual

            elif value.month_date == "January" and value.year_date=='24':
                custom_data['jan_3'] = value.amount_residual
            elif value.month_date == "Feburary" and value.year_date=='24':
                custom_data['feb_3'] = value.amount_residual
            elif value.month_date == "March"and value.year_date=='24':
                custom_data['mar_3'] = value.amount_residual
            elif value.month_date == "April" and value.year_date=='24':
                custom_data['apr_3'] = value.amount_residual
            elif value.month_date == "May" and value.year_date=='24':
                custom_data['may_3'] = value.amount_residual
            elif value.month_date == "June" and value.year_date=='24':
                custom_data['jun_3'] = value.amount_residual
            elif value.month_date == "July" and value.year_date=='24':
                custom_data['jul_3'] = value.amount_residual
            elif value.month_date == "August" and value.year_date=='24':
                custom_data['aug_3'] = value.amount_residual
            elif value.month_date == "September" and value.year_date=='24':
                custom_data['sep_3'] = value.amount_residual
            elif value.month_date == "October" and value.year_date=='24':
                custom_data['oct_3'] = value.amount_residual
            elif value.month_date == "November" and value.year_date=='24':
                custom_data['nov_3'] = value.amount_residual
            elif value.month_date == "December" and value.year_date=='24':
                custom_data['dec_3'] = value.amount_residual
            
            custom_data['total_amount']=value.amount_residual
            
           

            temp_lst.append(custom_data)
            #raise UserError(custom_data["apr_3"])

        for element in temp_lst:
            temp_dict={
                        "record_id":'',
                        "roll_no":0,
                        "name":'',
                        "full_roll_number":" ",
                        "student_batch":'',
                        "student_branch":"",
                        "student_class":'',
                        "withdrawn_status":"",
                        "leaving_reason":"",
                        "remarks":"",
                        "withdrawn_date":'',
                        "app_date":'',
                        "jan": 0,
                        "feb": 0,
                        "mar": 0,
                        "apr":0,
                        "may":0,
                        "jun": 0,
                        "jul":0,
                        "aug":0,
                        "sep": 0,
                        "oct": 0,
                        "nov": 0,
                        "dec": 0,

                        "jan_2": 0,
                        "feb_2": 0,
                        "mar_2": 0,
                        "apr_2":0,
                        "may_2":0,
                        "jun_2": 0,
                        "jul_2":0,
                        "aug_2":0,
                        "sep_2": 0,
                        "oct_2": 0,
                        "nov_2": 0,
                        "dec_2": 0,

                        "jan_3": 0,
                        "feb_3": 0,
                        "mar_3": 0,
                        "apr_3":0,
                        "may_3":0,
                        "jun_3": 0,
                        "jul_3":0,
                        "aug_3":0,
                        "sep_3": 0,
                        "oct_3": 0,
                        "nov_3": 0,
                        "dec_3": 0,
                        "total_amount":0
                    }
           
            temp_dict["jan"]           =   element["jan"]
            temp_dict["feb"]           =   element["feb"]
            temp_dict["mar"]           =   element["mar"]
            temp_dict["jan"]           =   element["jan"]
            temp_dict["apr"]           =   element["apr"]
            temp_dict["may"]           =   element["may"]
            temp_dict["jun"]           =   element["jun"]
            temp_dict["jul"]           =   element["jul"]
            temp_dict["aug"]           =   element["aug"]
            temp_dict["sep"]           =   element["sep"]
            temp_dict["oct"]           =   element["oct"]
            temp_dict["nov"]           =   element["nov"]
            temp_dict["dec"]           =   element["dec"]

            temp_dict["jan_2"]           =   element["jan_2"]
            temp_dict["feb_2"]           =   element["feb_2"]
            temp_dict["mar_2"]           =   element["mar_2"]
            temp_dict["jan_2"]           =   element["jan_2"]
            temp_dict["apr_2"]           =   element["apr_2"]
            temp_dict["may_2"]           =   element["may_2"]
            temp_dict["jun_2"]           =   element["jun_2"]
            temp_dict["jul_2"]           =   element["jul_2"]
            temp_dict["aug_2"]           =   element["aug_2"]
            temp_dict["sep_2"]           =   element["sep_2"]
            temp_dict["oct_2"]           =   element["oct_2"]
            temp_dict["nov_2"]           =   element["nov_2"]
            temp_dict["dec_2"]           =   element["dec_2"]

            temp_dict["jan_3"]           =   element["jan_3"]
            temp_dict["feb_3"]           =   element["feb_3"]
            temp_dict["mar_3"]           =   element["mar_3"]
            temp_dict["apr_3"]           =   element["apr_3"]
            temp_dict["may_3"]           =   element["may_3"]
            temp_dict["jun_3"]           =   element["jun_3"]
            temp_dict["jul_3"]           =   element["jul_3"]
            temp_dict["aug_3"]           =   element["aug_3"]
            temp_dict["sep_3"]           =   element["sep_3"]
            temp_dict["oct_3"]           =   element["oct_3"]
            temp_dict["nov_3"]           =   element["nov_3"]
            temp_dict["dec_3"]           =   element["dec_3"]

            temp_dict["record_id"]     =   element["record_id"]
            temp_dict["roll_no"]       =   element["roll_no"]
            temp_dict["full_roll_number"]  =   element["full_roll_number"]
            temp_dict["name"]          =   element["name"]
            temp_dict["student_batch"] =   element["student_batch"]
            temp_dict["student_branch"]=   element["student_branch"]
            temp_dict["student_class"] =   element["student_class"]
            temp_dict["withdrawn_status"]= element["withdrawn_status"]
            temp_dict["leaving_reason"]=   element["leaving_reason"]
            temp_dict["remarks"]        =  element["remarks"]
            temp_dict["withdrawn_date"] =  element["withdrawn_date"]
            temp_dict["app_date"]       =  element["app_date"]
            temp_dict["total_amount"]   =  element["total_amount"]

            #raise UserError(temp_dict["apr_3"])

            if element["full_roll_number"] not in invoice_check:
                        invoice_check.append(element["full_roll_number"])
                        #raise UserError(temp_dict["apr_3"])
                        final_lst.append(temp_dict)
            
            

            else:
                index = invoice_check.index(element["full_roll_number"])
                final_lst[index]["jan"]  +=    temp_dict["jan"]
                final_lst[index]["feb"]  +=    temp_dict["feb"]  
                final_lst[index]["mar"]  +=    temp_dict["mar"]  
                final_lst[index]["apr"]  +=    temp_dict["apr"]  
                final_lst[index]["may"]  +=    temp_dict["may"] 
                final_lst[index]["jun"]  +=    temp_dict["jun"] 
                final_lst[index]["jul"]  +=    temp_dict["jul"] 
                final_lst[index]["aug"]  +=    temp_dict["aug"]
                final_lst[index]["sep"]  +=    temp_dict["sep"]
                final_lst[index]["oct"]  +=    temp_dict["oct"]
                final_lst[index]["nov"]  +=    temp_dict["nov"]
                final_lst[index]["dec"]  +=    temp_dict["dec"]

                final_lst[index]["jan_2"]  +=    temp_dict["jan_2"]
                final_lst[index]["feb_2"]  +=    temp_dict["feb_2"]  
                final_lst[index]["mar_2"]  +=    temp_dict["mar_2"]  
                final_lst[index]["apr_2"]  +=    temp_dict["apr_2"]  
                final_lst[index]["may_2"]  +=    temp_dict["may_2"] 
                final_lst[index]["jun_2"]  +=    temp_dict["jun_2"] 
                final_lst[index]["jul_2"]  +=    temp_dict["jul_2"] 
                final_lst[index]["aug_2"]  +=    temp_dict["aug_2"]
                final_lst[index]["sep_2"]  +=    temp_dict["sep_2"]
                final_lst[index]["oct_2"]  +=    temp_dict["oct_2"]
                final_lst[index]["nov_2"]  +=    temp_dict["nov_2"]
                final_lst[index]["dec_2"]  +=    temp_dict["dec_2"]

                final_lst[index]["jan_3"]  +=    temp_dict["jan_3"]
                final_lst[index]["feb_3"]  +=    temp_dict["feb_3"]  
                final_lst[index]["mar_3"]  +=    temp_dict["mar_3"]  
                final_lst[index]["apr_3"]  +=    temp_dict["apr_3"]  
                final_lst[index]["may_3"]  +=    temp_dict["may_3"] 
                final_lst[index]["jun_3"]  +=    temp_dict["jun_3"] 
                final_lst[index]["jul_3"]  +=    temp_dict["jul_3"] 
                final_lst[index]["aug_3"]  +=    temp_dict["aug_3"]
                final_lst[index]["sep_3"]  +=    temp_dict["sep_3"]
                final_lst[index]["oct_3"]  +=    temp_dict["oct_3"]
                final_lst[index]["nov_3"]  +=    temp_dict["nov_3"]
                final_lst[index]["dec_3"]  +=    temp_dict["dec_3"]

                #raise UserError(final_lst[index]["apr_3"])

                final_lst[index]["total_amount"]   +=    temp_dict["total_amount"]  
        # raise UserError(str(final_lst))
        # desired_name = ''+'\n'
        
        # for item in temp_list_2:
        #     desired_name += str(item['name'])+"========"+str(item['full_roll_number'])+"========"+str(item['total_amount'])+'\n'

        # raise UserError(str(desired_name))
        # invoice_checks_2 = []
        # final_list_2 = []
        temp_list_2 = []
        for value in inv_ids:
            

            custom_dataa = {
                       "full_roll_number":'',
                        "jan": 0,
                        "feb": 0,
                        "mar": 0,
                        "apr":0,
                        "may":0,
                        "jun": 0,
                        "jul":0,
                        "aug":0,
                        "sep": 0,
                        "oct": 0,
                        "nov": 0,
                        "dec": 0,

                        "jan_2": 0,
                        "feb_2": 0,
                        "mar_2": 0,
                        "apr_2":0,
                        "may_2":0,
                        "jun_2": 0,
                        "jul_2":0,
                        "aug_2":0,
                        "sep_2": 0,
                        "oct_2": 0,
                        "nov_2": 0,
                        "dec_2": 0,

                        "jan_3": 0,
                        "feb_3": 0,
                        "mar_3": 0,
                        "apr_3":0,
                        "may_3":0,
                        "jun_3": 0,
                        "jul_3":0,
                        "aug_3":0,
                        "sep_3": 0,
                        "oct_3": 0,
                        "nov_3": 0,
                        "dec_3": 0,
                        "total_amount":0
                    }

            # raise UserError((value.student_id.olf_udid) )
            custom_dataa['full_roll_number'] = value.student_ids.olf_udid 
            if value.month_date == "January" and value.year_date=='22':
                custom_dataa['jan'] = value.amount_residual
            elif value.month_date == "Feburary" and value.year_date=='22':
                custom_dataa['feb'] = value.amount_residual
            elif value.month_date == "March"and value.year_date=='22':
                custom_dataa['mar'] = value.amount_residual
            elif value.month_date == "April" and value.year_date=='22':
                custom_dataa['apr'] = value.amount_residual
            elif value.month_date == "May" and value.year_date=='22':
                custom_dataa['may'] = value.amount_residual
            elif value.month_date == "June" and value.year_date=='22':
                custom_dataa['jun'] = value.amount_residual
            elif value.month_date == "July" and value.year_date=='22':
                custom_dataa['jul'] = value.amount_residual
            elif value.month_date == "August" and value.year_date=='22':
                custom_dataa['aug'] = value.amount_residual
            elif value.month_date == "September" and value.year_date=='22':
                custom_dataa['sep'] = value.amount_residual
            elif value.month_date == "October" and value.year_date=='22':
                custom_dataa['oct'] = value.amount_residual
            elif value.month_date == "November" and value.year_date=='22':
                custom_dataa['nov'] = value.amount_residual
            elif value.month_date == "December" and value.year_date=='22':
                custom_dataa['dec'] = value.amount_residual

            elif value.month_date == "January" and value.year_date=='23':
                custom_dataa['jan_2'] = value.amount_residual
            elif value.month_date == "Feburary" and value.year_date=='23':
                custom_dataa['feb_2'] = value.amount_residual
            elif value.month_date == "March"and value.year_date=='23':
                custom_dataa['mar_2'] = value.amount_residual
            elif value.month_date == "April" and value.year_date=='23':
                custom_dataa['apr_2'] = value.amount_residual
            elif value.month_date == "May" and value.year_date=='23':
                custom_dataa['may_2'] = value.amount_residual
            elif value.month_date == "June" and value.year_date=='23':
                custom_dataa['jun_2'] = value.amount_residual
            elif value.month_date == "July" and value.year_date=='23':
                custom_dataa['jul_2'] = value.amount_residual
            elif value.month_date == "August" and value.year_date=='23':
                custom_dataa['aug_2'] = value.amount_residual
            elif value.month_date == "September" and value.year_date=='23':
                custom_dataa['sep_2'] = value.amount_residual
            elif value.month_date == "October" and value.year_date=='23':
                custom_dataa['oct_2'] = value.amount_residual
            elif value.month_date == "November" and value.year_date=='23':
                custom_dataa['nov_2'] = value.amount_residual
            elif value.month_date == "December" and value.year_date=='23':
                custom_dataa['dec_2'] = value.amount_residual

            elif value.month_date == "January" and value.year_date=='24':
                custom_dataa['jan_3'] = value.amount_residual
            elif value.month_date == "Feburary" and value.year_date=='24':
                custom_dataa['feb_3'] = value.amount_residual
            elif value.month_date == "March"and value.year_date=='24':
                custom_dataa['mar_3'] = value.amount_residual
            elif value.month_date == "April" and value.year_date=='24':
                custom_dataa['apr_3'] = value.amount_residual
            elif value.month_date == "May" and value.year_date=='24':
                custom_dataa['may_3'] = value.amount_residual
            elif value.month_date == "June" and value.year_date=='24':
                custom_dataa['jun_3'] = value.amount_residual
            elif value.month_date == "July" and value.year_date=='24':
                custom_dataa['jul_3'] = value.amount_residual
            elif value.month_date == "August" and value.year_date=='24':
                custom_dataa['aug_3'] = value.amount_residual
            elif value.month_date == "September" and value.year_date=='24':
                custom_dataa['sep_3'] = value.amount_residual
            elif value.month_date == "October" and value.year_date=='24':
                custom_dataa['oct_3'] = value.amount_residual
            elif value.month_date == "November" and value.year_date=='24':
                custom_dataa['nov_3'] = value.amount_residual
            elif value.month_date == "December" and value.year_date=='24':
                custom_dataa['dec_3'] = value.amount_residual
            
            custom_dataa['total_amount']=value.amount_residual
            
            #raise UserError(custom_dataa['apr_3'])
            temp_list_2.append(custom_dataa)
        # raise UserError(str(temp_list_2))
        

        
        for element in temp_list_2:
            temp_dct={
                        "full_roll_number":'',
                        "jan": 0,
                        "feb": 0,
                        "mar": 0,
                        "apr":0,
                        "may":0,
                        "jun": 0,
                        "jul":0,
                        "aug":0,
                        "sep": 0,
                        "oct": 0,
                        "nov": 0,
                        "dec": 0,

                        "jan_2": 0,
                        "feb_2": 0,
                        "mar_2": 0,
                        "apr_2":0,
                        "may_2":0,
                        "jun_2": 0,
                        "jul_2":0,
                        "aug_2":0,
                        "sep_2": 0,
                        "oct_2": 0,
                        "nov_2": 0,
                        "dec_2": 0,

                        "jan_3": 0,
                        "feb_3": 0,
                        "mar_3": 0,
                        "apr_3":0,
                        "may_3":0,
                        "jun_3": 0,
                        "jul_3":0,
                        "aug_3":0,
                        "sep_3": 0,
                        "oct_3": 0,
                        "nov_3": 0,
                        "dec_3": 0,
                        "total_amount":0
                    }
            temp_dct["full_roll_number"]  =   element["full_roll_number"]
            temp_dct["jan"]           =   element["jan"]
            temp_dct["feb"]           =   element["feb"]
            temp_dct["mar"]           =   element["mar"]
            temp_dct["jan"]           =   element["jan"]
            temp_dct["apr"]           =   element["apr"]
            temp_dct["may"]           =   element["may"]
            temp_dct["jun"]           =   element["jun"]
            temp_dct["jul"]           =   element["jul"]
            temp_dct["aug"]           =   element["aug"]
            temp_dct["sep"]           =   element["sep"]
            temp_dct["oct"]           =   element["oct"]
            temp_dct["nov"]           =   element["nov"]
            temp_dct["dec"]           =   element["dec"]

            temp_dct["jan_2"]           =   element["jan_2"]
            temp_dct["feb_2"]           =   element["feb_2"]
            temp_dct["mar_2"]           =   element["mar_2"]
            temp_dct["jan_2"]           =   element["jan_2"]
            temp_dct["apr_2"]           =   element["apr_2"]
            temp_dct["may_2"]           =   element["may_2"]
            temp_dct["jun_2"]           =   element["jun_2"]
            temp_dct["jul_2"]           =   element["jul_2"]
            temp_dct["aug_2"]           =   element["aug_2"]
            temp_dct["sep_2"]           =   element["sep_2"]
            temp_dct["oct_2"]           =   element["oct_2"]
            temp_dct["nov_2"]           =   element["nov_2"]
            temp_dct["dec_2"]           =   element["dec_2"]

            temp_dct["jan_3"]           =   element["jan_3"]
            temp_dct["feb_3"]           =   element["feb_3"]
            temp_dct["mar_3"]           =   element["mar_3"]
            temp_dct["apr_3"]           =   element["apr_3"]
            temp_dct["may_3"]           =   element["may_3"]
            temp_dct["jun_3"]           =   element["jun_3"]
            temp_dct["jul_3"]           =   element["jul_3"]
            temp_dct["aug_3"]           =   element["aug_3"]
            temp_dct["sep_3"]           =   element["sep_3"]
            temp_dct["oct_3"]           =   element["oct_3"]
            temp_dct["nov_3"]           =   element["nov_3"]
            temp_dct["dec_3"]           =   element["dec_3"]
            temp_dct["total_amount"]   =  element["total_amount"]

            #raise UserError(temp_dct["apr_3"])

            if element["full_roll_number"] in invoice_check:
            
                index = invoice_check.index(element["full_roll_number"])
                # raise UserError(index)
                final_lst[index]["jan"]  +=    temp_dct["jan"]
                final_lst[index]["feb"]  +=    temp_dct["feb"]  
                final_lst[index]["mar"]  +=    temp_dct["mar"]  
                final_lst[index]["apr"]  +=    temp_dct["apr"]  
                final_lst[index]["may"]  +=    temp_dct["may"] 
                final_lst[index]["jun"]  +=    temp_dct["jun"] 
                final_lst[index]["jul"]  +=    temp_dct["jul"] 
                final_lst[index]["aug"]  +=    temp_dct["aug"]
                final_lst[index]["sep"]  +=    temp_dct["sep"]
                final_lst[index]["oct"]  +=    temp_dct["oct"]
                final_lst[index]["nov"]  +=    temp_dct["nov"]
                final_lst[index]["dec"]  +=    temp_dct["dec"]

                final_lst[index]["jan_2"]  +=    temp_dct["jan_2"]
                final_lst[index]["feb_2"]  +=    temp_dct["feb_2"]  
                final_lst[index]["mar_2"]  +=    temp_dct["mar_2"]  
                final_lst[index]["apr_2"]  +=    temp_dct["apr_2"]  
                final_lst[index]["may_2"]  +=    temp_dct["may_2"] 
                final_lst[index]["jun_2"]  +=    temp_dct["jun_2"] 
                final_lst[index]["jul_2"]  +=    temp_dct["jul_2"] 
                final_lst[index]["aug_2"]  +=    temp_dct["aug_2"]
                final_lst[index]["sep_2"]  +=    temp_dct["sep_2"]
                final_lst[index]["oct_2"]  +=    temp_dct["oct_2"]
                final_lst[index]["nov_2"]  +=    temp_dct["nov_2"]
                final_lst[index]["dec_2"]  +=    temp_dct["dec_2"]

                final_lst[index]["jan_3"]  +=    temp_dct["jan_3"]
                final_lst[index]["feb_3"]  +=    temp_dct["feb_3"]  
                final_lst[index]["mar_3"]  +=    temp_dct["mar_3"]  
                final_lst[index]["apr_3"]  +=    temp_dct["apr_3"]  
                final_lst[index]["may_3"]  +=    temp_dct["may_3"] 
                final_lst[index]["jun_3"]  +=    temp_dct["jun_3"] 
                final_lst[index]["jul_3"]  +=    temp_dct["jul_3"] 
                final_lst[index]["aug_3"]  +=    temp_dct["aug_3"]
                final_lst[index]["sep_3"]  +=    temp_dct["sep_3"]
                final_lst[index]["oct_3"]  +=    temp_dct["oct_3"]
                final_lst[index]["nov_3"]  +=    temp_dct["nov_3"]
                final_lst[index]["dec_3"]  +=    temp_dct["dec_3"]
                final_lst[index]["total_amount"]   +=    temp_dct["total_amount"]  

            

        # desired_dict={}

        # desired_name = ''+'\n'
        
        # for item in temp_list_2:
        #     desired_name += str(item['full_roll_number'])+"========"+str(item['total_amount'])+'\n'

        # raise UserError(str(desired_name))
        
 
        lines=[]
        # raise UserError(str(full_final_lst))
        for mov in final_lst:
            # if mov['record_id'] in full_final_lst:
            #     raise UserError(str(mov))
                mvl=self.env['account.report.move.line'].create({
                    "record_id":mov['record_id'],
                    "roll_no":mov['roll_no'],
                    "name":mov['name'],
                    "student_batch":mov['student_batch'],
                    "student_branch":mov['student_branch'],
                    "student_class":mov['student_class'],
                    "withdrawn_status":mov['withdrawn_status'],
                    "leaving_reason":mov['leaving_reason'],
                    "remarks":mov['remarks'],
                    "withdrawn_date":mov['withdrawn_date'],
                   "app_date":mov['app_date'],
                    "full_roll_number":mov['full_roll_number'],
                    "jan":mov['jan'],
                    "feb":mov['feb'],
                    "mar":mov['mar'],
                    "apr":mov['apr'],
                    "may":mov['may'],
                    "jun":mov['jun'],
                    "jul":mov['jul'],
                    "aug":mov['aug'],
                    "sep":mov['sep'],
                    "oct":mov['oct'],
                    "nov":mov['nov'],
                    "dec":mov['dec'],

                    "jan_2":mov['jan_2'],
                    "feb_2":mov['feb_2'],
                    "mar_2":mov['mar_2'],
                    "apr_2":mov['apr_2'],
                    "may_2":mov['may_2'],
                    "jun_2":mov['jun_2'],
                    "jul_2":mov['jul_2'],
                    "aug_2":mov['aug_2'],
                    "sep_2":mov['sep_2'],
                    "oct_2":mov['oct_2'],
                    "nov_2":mov['nov_2'],
                    "dec_2":mov['dec_2'],

                    "jan_3":mov['jan_3'],
                    "feb_3":mov['feb_3'],
                    "mar_3":mov['mar_3'],
                    "apr_3":mov['apr_3'],
                    "may_3":mov['may_3'],
                    "jun_3":mov['jun_3'],
                    "jul_3":mov['jul_3'],
                    "aug_3":mov['aug_3'],
                    "sep_3":mov['sep_3'],
                    "oct_3":mov['oct_3'],
                    "nov_3":mov['nov_3'],
                    "dec_3":mov['dec_3'],

                    "total_amount": round(mov['total_amount'] or 0, 2)
            
                    
        
                })
                #raise UserError(mvl)
                lines.append(mvl.id)
           
        
        # desired_name = ''+'\n'
        
        # for item in final_lst:
        #     desired_name += str(item['full_roll_number'])+"========"+str(item['total_amount'])+'\n'

        # raise UserError(str(desired_name))
       

        self.write({
            "account_report_line":[(6,0,lines)]
        }

        )
        # raise UserError(str(final_lst))
       
       
        

        
            
    
    def action_print_excel_report(self):
        global first_date 
        global last_date
        

        self.action_print_report()
        
        
        if xlwt:

            
            filename = 'RECEIVABLE OF WITHDRAWAL STUDENTS.xls'
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('Receivables of Withdrawl Std')
            text_style = xlwt.easyxf('align: horiz left')
            

            
            style_title = xlwt.easyxf(
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            red_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour tan;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            yellow_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            lime_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour lime;'
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")

            grand_heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;'
                              'font: colour black, bold True;')

            heading_style = xlwt.easyxf('align: vertical center,horiz center;')
            
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'dd/mm/yyyy'

            worksheet.write_merge(0, 1, 0, 5,"LACAS SCHOOL NETWORK ",style=style_title)
            worksheet.write_merge(0, 1, 6, 11, "RECEIVABLE OF WITHDRAWAL STUDENTS", style=style_title)
            
            

            worksheet.write_merge(2,3,0,0,"Sr.No", style=red_style_title)
            worksheet.write_merge(2,3,1,3,"ID",style=red_style_title)
            worksheet.write_merge(2,3,4,5,"App Date",style=red_style_title)
            worksheet.write_merge(2,3,6,7,"olf ID",style=red_style_title)
            worksheet.write_merge(2,3,8,9,"6 Digit Roll No",style=yellow_style_title)
            worksheet.write_merge(2,3,10,11,"Name",style=red_style_title)
            worksheet.write_merge(2,3,12,13,"Batch #",style=red_style_title)
            worksheet.write_merge(2,3,14,16,"Branch",style=red_style_title)
            worksheet.write_merge(2,3,17,18,"Class",style=red_style_title)
            worksheet.write_merge(2,3,19,20,"withdrawn Status", red_style_title)
            worksheet.write_merge(2,3,21,22,"Leaving Reaon", red_style_title)
            worksheet.write_merge(2,3,23,24,"Remarks", red_style_title)
            worksheet.write_merge(2,3,25,26,"Withdrawn DT", red_style_title)


            v_from_month=datetime.strptime(str(first_date), "%Y-%m-%d").strftime('%m')
            v_from_year=datetime.strptime(str(first_date), "%Y-%m-%d").strftime('%y')

            v_to_month=datetime.strptime(str(last_date), "%Y-%m-%d").strftime('%m')
            v_to_year=datetime.strptime(str(last_date), "%Y-%m-%d").strftime('%y')

            months= {
                1:['01','JAN-22',10,'22'],
                2:['02','FEB-22',20,'22'],
                3:['03','MAR-22',30,'22'],
                4:['04','APR-22',40,'22'],
                5:['05','MAY-22',50,'22'],
                6:['06','JUN-22',60,'22'],
                7:['07','JUL-22',70,'22'],
                8:['08','AUG-22',80,'22'],
                9:['09','SEP-22',90,'22'],
                10:['10','OCT-22',100,'22'],
                11:['11','NOV-22',110,'22'],
                12:['12','DEC-22',120,'22'],
                13:['01','JAN-23',130,'23'],
                14:['02','FEB-23',140,'23'],
                15:['03','MAR-23',150,'23'],
                16:['04','APR-23',160,'23'],
                17:['05','MAY-23',170,'23'],
                18:['06','JUN-23',180,'23'],
                19:['07','JUL-23',190,'23'],
                20:['08','AUG-23',200,'23'],
                21:['09','SEP-23',200,'23'],
                22:['10','OCT-23',200,'23'],
                23:['11','NOV-23',200,'23'],
                24:['12','DEC-23',200,'23'],

                25:['01','JAN-24',130,'24'],
                26:['02','FEB-24',140,'24'],
                27:['03','MAR-24',150,'24'],
                28:['04','APR-24',160,'24'],
                29:['05','MAY-24',170,'24'],
                30:['06','JUN-24',180,'24'],
                31:['07','JUL-24',190,'24'],
                32:['08','AUG-24',200,'24'],
                33:['09','SEP-24',200,'24'],
                34:['10','OCT-24',200,'24'],
                35:['11','NOV-24',200,'24'],
                36:['12','DEC-24',200,'24'],
                }
            range_start = 0
            range_stop = 0
            # raise UserError(v_to)
            for key, value in months.items():
                if value[0] == v_from_month and value[3] == v_from_year:
                    range_start = key
                if value[0] == v_to_month and value[3] == v_to_year:

                    range_stop = key

            col = 27
            
      
            for i in range(range_start,range_stop+1):
      
                worksheet.write_merge(2,3,col,col+1,months[i][1],red_style_title)
                # worksheet.write_merge(row,row,col,col+1,months[i][2])
                col+=2

            worksheet.write_merge(2,3,col,col+1,"Total", lime_style_title)   
            
                # print('col:',months[i][1], 'data:',months[i][2])

            # row = 4
            # sno = 1
        
            column = 27
            row = 4
            sn=1
            for rec in self.account_report_line:
                

                
                if rec:

                    column = 27

                    worksheet.write(row,0,sn)
                    worksheet.write_merge(row,row,1,3,rec.record_id,heading_style)
                    worksheet.write_merge(row,row,4,5,rec.app_date,heading_style)
                    worksheet.write_merge(row,row,6,7,rec.roll_no,heading_style)
                    worksheet.write_merge(row,row,8,9,rec.full_roll_number,text_style)
                    worksheet.write_merge(row,row,10,11,rec.name,heading_style)
                    worksheet.write_merge(row,row,12,13,rec.student_batch,heading_style)
                    worksheet.write_merge(row,row,14,16,rec.student_branch,heading_style)
                    worksheet.write_merge(row,row,17,18,rec.student_class,heading_style)
                    worksheet.write_merge(row,row,19,20,rec.withdrawn_status,heading_style)
                    worksheet.write_merge(row,row,21,22,rec.leaving_reason,heading_style)
                    worksheet.write_merge(row,row,23,24,rec.remarks,heading_style)
                    worksheet.write_merge(row,row,25,26,rec.withdrawn_date,heading_style)

                    data_month= {
                        1:['01','JAN-22',rec.jan,'22'],
                        2:['02','FEB-22',rec.feb,'22'],
                        3:['03','MAR-22',rec.mar,'22'],
                        4:['04','APR-22',rec.apr,'22'],
                        5:['05','MAY-22',rec.may,'22'],
                        6:['06','JUN-22',rec.jun,'22'],
                        7:['07','JUL-22',rec.jul,'22'],
                        8:['08','AUG-22',rec.aug,'22'],
                        9:['09','SEP-22',rec.sep,'22'],
                        10:['10','OCT-22',rec.oct,'22'],
                        11:['11','NOV-22',rec.nov,'22'],
                        12:['12','DEC-22',rec.dec,'22'],
                        13:['01','JAN-23',rec.jan_2,'23'],
                        14:['02','FEB-23',rec.feb_2,'23'],
                        15:['03','MAR-23',rec.mar_2,'23'],
                        16:['04','APR-23',rec.apr_2,'23'],
                        17:['05','MAY-23',rec.may_2,'23'],
                        18:['06','JUN-23',rec.jun_2,'23'],
                        19:['07','JUL-23',rec.jul_2,'23'],
                        20:['08','AUG-23',rec.aug_2,'23'],
                        21:['09','SEP-23',rec.sep_2,'23'],
                        22:['10','OCT-23',rec.oct_2,'23'],
                        23:['11','NOV-23',rec.nov_2,'23'],
                        24:['12','DEC-23',rec.dec_2,'23'],

                        25:['01','JAN-24',rec.jan_3,'24'],
                        26:['02','FEB-24',rec.feb_3,'24'],
                        27:['03','MAR-24',rec.mar_3,'24'],
                        28:['04','APR-24',rec.apr_3,'24'],
                        29:['05','MAY-24',rec.may_3,'24'],
                        30:['06','JUN-24',rec.jun_3,'24'],
                        31:['07','JUL-24',rec.jul_3,'24'],
                        32:['08','AUG-24',rec.aug_3,'24'],
                        33:['09','SEP-24',rec.sep_3,'24'],
                        34:['10','OCT-24',rec.oct_3,'24'],
                        34:['11','NOV-24',rec.nov_3,'24'],
                        36:['12','DEC-24',rec.dec_3,'24'],
                    }
                    range_start = 0
                    range_stop = 0
                  
                    for key, value in data_month.items():
                        if value[0] == v_from_month and value[3] == v_from_year:
                            range_start = key
                        if value[0] == v_to_month and value[3] == v_to_year:
                            range_stop = key
                    

                    for i in range(range_start,range_stop+1):
                        # raise UserError(column)
                        worksheet.write_merge(row,row,column,column+1,data_month[i][2],heading_style)
                        # worksheet.write_merge(row,row,column,column+1,rec.total_amount)
                        # lst.append([row_1,row_1,column,column+1])
                      
                        column+=2
                    if rec.total_amount != 0:
                        worksheet.write_merge(row,row,column,column+1,rec.total_amount,heading_style)
                      
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
        