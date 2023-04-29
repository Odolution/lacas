
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

class AccountMoveReport(models.TransientModel):
    _name = 'account.charges.report.move.line'


    
  
    std_roll_no=fields.Char('Roll No.')
    std_f_name=fields.Char('First Name')
    std_m_name=fields.Char('Middle Name.')
    std_l_name=fields.Char('Last Name')
    special_charges=fields.Char('Specialization_Name')
    department=fields.Char('Department')
    program_name=fields.Char('Program Name')
    amount_charged=fields.Integer('Amount Charged')
    academic_level=fields.Char('Academic Level')
    section_std=fields.Char('Section')
    remarks_std=fields.Char('Remark')

  
    
   

class SiblingsReportWizard(models.TransientModel):
    _name="charges.report.wizard"
    _description='Specialization Charges Wizard'

    
    account_charges_report_line=fields.Many2many('account.charges.report.move.line', string='Account report Line')
 
    all_batch=fields.Boolean(string=" Select All Batches")
    one_batch=fields.Selection(
        [('old_batch','Session 2022-2023'),
        ('new_batch','Session 2023-2024')]
        ,string="Select any one Batch")

    def _batch_constrains(self):
      

        if self.all_batch==True and self.one_batch!=False:
                raise ValidationError(_('Sorry, You Must select one option...'))
             

        elif self.one_batch!=False and self.all_batch==True:
                raise ValidationError(_('Sorry, You Must select one option...'))

  

  
    
    def action_print_report(self):

        tuition_plan=self.env['tuition.plan'].search([])
        lines=[]
        # roll_no=''
        # f_name=''
        # m_name=''
        # l_name=''
        # specialization=''
        # program=''
        # classs=''
        # sec=''
        # dept=''
        # price=0
        # remarks=''

        if self.all_batch:
            for rec in tuition_plan:
                if rec.line_ids:
                    for line in rec.line_ids:
                        if line.product_id.x_studio_code:
                            roll_no=rec.student_id.facts_udid
                            f_name=rec.student_id.first_name
                            m_name=rec.student_id.middle_name
                            l_name=rec.student_id.last_name
                            specialization=line.product_id.name
                            price=line.unit_price
                            splitted_name=specialization.split(' ')
                            if len(splitted_name)>2:
                                program=splitted_name[0]+" "+splitted_name[1]
                            if rec.student_id.homeroom:
                                wholename=rec.student_id.homeroom
                                splitted_name=wholename.split('-')
                                if len(splitted_name)>2:
                                    classs=splitted_name[0]+"-"+splitted_name[1]
                                    sec=splitted_name[2]
                                elif len(splitted_name)>1:
                                    classs=splitted_name[0]
                                    sec=splitted_name[1]
                                elif len(splitted_name)>0:
                                        classs=splitted_name[0]
                            if rec.student_id.school_ids:
                                if rec.student_id.enrollment_history_ids:
                                    enroll_history=rec.student_id.enrollment_history_ids
                                    lst=[]
                                    for linez in enroll_history:
                                        lst.append(linez.program_id.name)
                                    dept=lst[0]
            

                            mvl=self.env['account.charges.report.move.line'].create({
                                    
                                    "std_roll_no":roll_no,
                                    "std_f_name":f_name,
                                    "std_m_name":m_name,
                                    "std_l_name":l_name,
                                    "special_charges":specialization,
                                    "department":dept,
                                    "program_name":program,
                                    "amount_charged":price,
                                    "academic_level":classs,
                                    "section_std":sec,
                                    "remarks_std":'',



                                        

                        })
                            lines.append(mvl.id)
                            

                

                            
            
            self.write({
                "account_charges_report_line":[(6,0,lines)]
            })

        else:
            if self.one_batch=='old_batch':
                old_batch_val=dict(self._fields['one_batch'].selection).get(self.one_batch)
                for rec in tuition_plan:
                    if rec.student_id.x_studio_batchsession==old_batch_val:
                      
                        if rec.line_ids:
                            for line in rec.line_ids:
                                if line.product_id.x_studio_code:
                                    roll_no=rec.student_id.facts_udid
                                    f_name=rec.student_id.first_name
                                    m_name=rec.student_id.middle_name
                                    l_name=rec.student_id.last_name
                                    specialization=line.product_id.name
                                    price=line.unit_price
                                    splitted_name=specialization.split(' ')
                                    if len(splitted_name)>2:
                                        program=splitted_name[0]+" "+splitted_name[1]
                                    if rec.student_id.homeroom:
                                        wholename=rec.student_id.homeroom
                                        splitted_name=wholename.split('-')
                                        if len(splitted_name)>2:
                                            classs=splitted_name[0]+"-"+splitted_name[1]
                                            sec=splitted_name[2]
                                        elif len(splitted_name)>1:
                                            classs=splitted_name[0]
                                            sec=splitted_name[1]
                                        elif len(splitted_name)>0:
                                                classs=splitted_name[0]
                                    if rec.student_id.school_ids:
                                        if rec.student_id.enrollment_history_ids:
                                            enroll_history=rec.student_id.enrollment_history_ids
                                            lst=[]
                                            for linez in enroll_history:
                                                lst.append(linez.program_id.name)
                                            dept=lst[0]
                    

                                    mvl=self.env['account.charges.report.move.line'].create({
                                            
                                            "std_roll_no":roll_no,
                                            "std_f_name":f_name,
                                            "std_m_name":m_name,
                                            "std_l_name":l_name,
                                            "special_charges":specialization,
                                            "department":dept,
                                            "program_name":program,
                                            "amount_charged":price,
                                            "academic_level":classs,
                                            "section_std":sec,
                                            "remarks_std":'',



                                                

                                })
                                
                                    lines.append(mvl.id)

                self.write({
                "account_charges_report_line":[(6,0,lines)]
            })

            elif self.one_batch=='new_batch':
                new_batch_val=dict(self._fields['one_batch'].selection).get(self.one_batch)
                for rec in tuition_plan:
                    if rec.student_id.x_studio_batchsession==new_batch_val:
                        if rec.line_ids:
                            for line in rec.line_ids:
                                if line.product_id.x_studio_code:
                                    roll_no=rec.student_id.facts_udid
                                    f_name=rec.student_id.first_name
                                    m_name=rec.student_id.middle_name
                                    l_name=rec.student_id.last_name
                                    specialization=line.product_id.name
                                    price=line.unit_price
                                    splitted_name=specialization.split(' ')
                                    if len(splitted_name)>2:
                                        program=splitted_name[0]+" "+splitted_name[1]
                                    if rec.student_id.homeroom:
                                        wholename=rec.student_id.homeroom
                                        splitted_name=wholename.split('-')
                                        if len(splitted_name)>2:
                                            classs=splitted_name[0]+"-"+splitted_name[1]
                                            sec=splitted_name[2]
                                        elif len(splitted_name)>1:
                                            classs=splitted_name[0]
                                            sec=splitted_name[1]
                                        elif len(splitted_name)>0:
                                                classs=splitted_name[0]
                                    if rec.student_id.school_ids:
                                        if rec.student_id.enrollment_history_ids:
                                            enroll_history=rec.student_id.enrollment_history_ids
                                            lst=[]
                                            for linez in enroll_history:
                                                lst.append(linez.program_id.name)
                                            dept=lst[0]
                    

                                    mvl=self.env['account.charges.report.move.line'].create({
                                            
                                            "std_roll_no":roll_no,
                                            "std_f_name":f_name,
                                            "std_m_name":m_name,
                                            "std_l_name":l_name,
                                            "special_charges":specialization,
                                            "department":dept,
                                            "program_name":program,
                                            "amount_charged":price,
                                            "academic_level":classs,
                                            "section_std":sec,
                                            "remarks_std":'',



                                                

                                })
                                    lines.append(mvl.id)
                self.write({
                "account_charges_report_line":[(6,0,lines)]
            })
                                    
                

                                    
                



  
       
    
    
    def action_print_charges_excel_report(self):
        self.action_print_report()
        
        
        if xlwt:


            filename='Specilaization Charges Report.xls'
            if self.all_batch==True:
                filename = 'All Batch Specilaization Charges Report.xls'
            elif self.one_batch:
                filename=dict(self._fields['one_batch'].selection).get(self.one_batch)+" "+'Specilaization Charges Report'+".xls"
         
               
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('Special Charges')
            

            
            style_title = xlwt.easyxf(
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")
            red_style_title = xlwt.easyxf('pattern: pattern solid, fore_colour pale_blue;'
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

            # worksheet.write_merge(0, 1, 0, 5,"LACAS SCHOOL NETWORK ",style=style_title)
            # worksheet.write_merge(0, 1, 6, 11, "SPECIALIZATION CHARGES REPORT", style=style_title)
            
            

            worksheet.write_merge(0,1,0,0,"Roll No.", style=red_style_title)
            worksheet.write_merge(0,1,1,1,"First Name",style=red_style_title)
            worksheet.write_merge(0,1,2,2,"Middle Name",style=red_style_title)
            worksheet.write_merge(0,1,3,3,"Last Name",style=red_style_title)
            worksheet.write_merge(0,1,4,4,"Department",style=red_style_title)
            worksheet.write_merge(0,1,5,5,"Program",style=red_style_title)
            worksheet.write_merge(0,1,6,6,"Specialization Name",style=red_style_title)
            worksheet.write_merge(0,1,7,7,"Amount Charged",style=red_style_title)
            worksheet.write_merge(0,1,8,8,"Academic Level",style=red_style_title)
            worksheet.write_merge(0,1,9,9,"Section", red_style_title)
            worksheet.write_merge(0,1,10,10,"Remarks", red_style_title)
      

            row=2
            for rec in self.account_charges_report_line:
                if rec.std_roll_no:
            
                    worksheet.write_merge(row,row,0,0,rec.std_roll_no, style=style_title)
                    worksheet.write_merge(row,row,1,1,rec.std_f_name,style=style_title)
                    worksheet.write_merge(row,row,2,2,rec.std_m_name,style=style_title)
                    worksheet.write_merge(row,row,3,3,rec.std_l_name,style=style_title)
                    worksheet.write_merge(row,row,4,4,rec.department,style=style_title)
                    worksheet.write_merge(row,row,5,5,rec.program_name,style=style_title)
                    worksheet.write_merge(row,row,6,6,rec.special_charges,style=style_title)
                    worksheet.write_merge(row,row,7,7,rec.amount_charged,style=style_title)
                    worksheet.write_merge(row,row,8,8,rec.academic_level,style=style_title)
                    worksheet.write_merge(row,row,9,9,rec.section_std, style_title)
                    worksheet.write_merge(row,row,10,10,rec.remarks_std, style_title)
              

   
                    row+=1
                  

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
        

   
                

           

























