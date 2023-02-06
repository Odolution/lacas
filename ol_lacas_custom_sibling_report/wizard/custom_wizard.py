
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
    _name = 'account.sibling.report.move.line'


    
  
    roll_no=fields.Char('Roll No.')
    parent_code=fields.Char('Parent Code')
    father_name=fields.Char('Father Name')
    f_phone_no=fields.Char('Phone No.')
    f_cnic=fields.Char('CNIC')
    f_address=fields.Char('Address')
    std_address=fields.Char('Student Address')
    no_of_child=fields.Integer('# of Children')
    m_cnic=fields.Char('Mother CNIC')
    mother_name=fields.Char('Mother Name')
    m_phone_no=fields.Char('Mother Phone No.')
    std_name=fields.Char('Student')
    emergency=fields.Char('Emergency Contact')
    std_gender=fields.Char('Gender')
    adm_date=fields.Char('Adm. Date')
    std_branch=fields.Char('Branch')
    std_batch=fields.Char('Batch')
    std_term=fields.Char('Term')
    std_class=fields.Char('Class')
    waiver_1=fields.Char('Waiver 1')
    waiver_2=fields.Char('Waiver 2')
  
    
   

class SiblingsReportWizard(models.TransientModel):
    _name="siblings.report.wizard"
    _description='Print Sibling Wizard'

    
    account_sibling_report_line=fields.Many2many('account.sibling.report.move.line', string='Account report Line')
 


  
    
    def action_print_report(self):
        student_data=self.env['school.family'].search([])
        lines=[]
        

    
        for rec in student_data:
            parent_code=''
            roll_no=''
            name=''
            phone=''
            tot_child=0
            street=''
            branch=''
            batch=''
            classs=''
            gender=''
            enroll_dt=''
            all_dis=''
            fcraw_dis=''
            f_name=''
            f_st=''
            f_ph=''
            m_name=''
            m_ph=''

            if len(rec.student_ids)>1:
                tot_child=(len(rec.student_ids))
                parent_code=rec.facts_udid
                li=[id for id in rec.student_ids]
                #li.sort(key=lambda x: x.grade_level_ids.x_studio_class)
                for grade in rec.student_ids.grade_level_ids:
                    li.sort(key=lambda x: grade.x_studio_class)
                for students in li:
                    roll_no=students.facts_udid
                    name=students.name
                    phone=students.phone
                    street=students.street
                    # branch=students.school_ids.name
                    # batch=students.x_studio_btachsesson 
                    classs=students.homeroom
                    gender=students.gender.name
                    if students.enrollment_state_ids:
                        for line in students.enrollment_state_ids:
                            enroll_dt=line.enrolled_date
                            if enroll_dt:
                                date=str(enroll_dt.day)
                                month=str(enroll_dt.month)
                                year=str(enroll_dt.year)
                                full_date=date+"-"+month+'-'+year
                                break
                    if students.enrollment_history_ids:
                        enroll_history=students.enrollment_history_ids
                        lst=[]
                        for hist in enroll_history:
                            lst.append(hist.program_id.name)
                        branch=lst[0]
                    if students.tuition_plan_ids:
                        for plans in students.tuition_plan_ids:
                            all_dis=plans.x_studio_discount_name_1 
                            fcraw_dis=plans.x_studio_fcraw_name
                    if students.relationship_ids:
                        for parents in students.relationship_ids:
                            if parents.relationship_type_id.name=='Father':
                                f_name=parents.individual_id.name 
                                f_st=parents.individual_id.street
                                f_ph=parents.individual_id.phone
                             
                            elif parents.relationship_type_id.name=='Mother':
                                m_name=parents.individual_id.name 
                                m_st=parents.individual_id.street
                                m_ph=parents.individual_id.phone
                        


                    mvl=self.env['account.sibling.report.move.line'].create({
                            
                        "roll_no":roll_no,
                        "parent_code":parent_code if parent_code else '',
                        "father_name":f_name if f_name else '-',
                        "f_phone_no":f_ph  if f_ph else '-',
                        "f_cnic":'',
                        "f_address":f_st  if f_st else '-',
                        "std_address":street  if street else '-',
                        "no_of_child":tot_child,
                        "m_cnic":"",
                        "mother_name":m_name  if m_name else '-',
                        "m_phone_no":m_ph  if m_ph else '-',
                        "emergency":phone,
                        "std_name":name,
                        "std_gender":gender if gender else "-",
                        "adm_date":full_date ,
                        "std_branch":branch,
                        "std_batch": "-",
                        "std_term":"",
                        "std_class":classs if classs else "-",
                        "waiver_1":all_dis if all_dis else '-',
                        "waiver_2":fcraw_dis if fcraw_dis else '-',
                                

                })
                    lines.append(mvl.id)

            # lst=[]
            # lst.append(mvl.roll_no)
            # lst.append(mvl.parent_code)
            # lst.append(mvl.father_name)
            # lst.append(mvl.f_phone_no)
            # lst.append(mvl.f_address)
            # lst.append(mvl.std_address)
            # lst.append(mvl.no_of_child)
            # lst.append(mvl.mother_name)
            # lst.append(mvl.adm_date)
            # lst.append(mvl.std_class)
            # raise UserError(lst)

                        
        
        self.write({
            "account_sibling_report_line":[(6,0,lines)]
        }

      )


  
       
    
    
    def action_print_excel_report(self):
        self.action_print_report()
        
        
        if xlwt:

            
            filename = 'SIBLING STUDENTS.xls'
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('Receivables of Withdrawl Std')
            

            
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

            worksheet.write_merge(0, 1, 0, 5,"LACAS SCHOOL NETWORK ",style=style_title)
            worksheet.write_merge(0, 1, 6, 11, "SIBLING STUDENTS REPORT", style=style_title)
            
            

            worksheet.write_merge(2,3,0,1,"Parent Code.", style=red_style_title)
            worksheet.write_merge(2,3,2,4,"Father Name",style=red_style_title)
            worksheet.write_merge(2,3,5,7,"Phone No",style=red_style_title)
            worksheet.write_merge(2,3,8,10,"CNIC",style=red_style_title)
            worksheet.write_merge(2,3,11,15,"Address",style=red_style_title)
            worksheet.write_merge(2,3,16,18,"# of Child",style=red_style_title)
            worksheet.write_merge(2,3,19,21,"Mother Name",style=red_style_title)
            worksheet.write_merge(2,3,22,24,"Mother CNIC",style=red_style_title)
            worksheet.write_merge(2,3,25,26,"Mother Phone No.",style=red_style_title)
            worksheet.write_merge(2,3,27,29,"Emergency Contact", red_style_title)
            worksheet.write_merge(2,3,30,31,"Roll No.", red_style_title)
            worksheet.write_merge(2,3,32,34,"Student Name", red_style_title)
            worksheet.write_merge(2,3,35,38,"Branch", red_style_title)
            worksheet.write_merge(2,3,39,40,"Class", red_style_title)
            worksheet.write_merge(2,3,41,43,"Batch", red_style_title)
            worksheet.write_merge(2,3,44,45,"Term", red_style_title)
            worksheet.write_merge(2,3,46,50,"Student Address", red_style_title)
            worksheet.write_merge(2,3,51,52,"Gender", red_style_title)
            worksheet.write_merge(2,3,53,54,"ADM Date", red_style_title)
            worksheet.write_merge(2,3,55,59,"Waiver 1", red_style_title)
            worksheet.write_merge(2,3,60,64,"Waiver 2", red_style_title)
            row=4
            for rec in self.account_sibling_report_line:
                    worksheet.write_merge(row,row,0,1,rec.parent_code, style=style_title)
                    worksheet.write_merge(row,row,2,4,rec.father_name,style=style_title)
                    worksheet.write_merge(row,row,5,7,rec.f_phone_no,style=style_title)
                    worksheet.write_merge(row,row,8,10,rec.f_cnic,style=style_title)
                    worksheet.write_merge(row,row,11,15,rec.f_address,style=style_title)
                    worksheet.write_merge(row,row,16,18,rec.no_of_child,style=style_title)
                    worksheet.write_merge(row,row,19,21,rec.mother_name,style=style_title)
                    worksheet.write_merge(row,row,22,24,rec.m_cnic,style=style_title)
                    worksheet.write_merge(row,row,25,26,rec.m_phone_no,style=style_title)
                    worksheet.write_merge(row,row,27,29,rec.emergency, style_title)
                    worksheet.write_merge(row,row,30,31,rec.roll_no, style_title)
                    worksheet.write_merge(row,row,32,34,rec.std_name, style_title)
                    worksheet.write_merge(row,row,35,38,rec.std_branch, style_title)
                    worksheet.write_merge(row,row,39,40,rec.std_class, style_title)
                    worksheet.write_merge(row,row,41,43,rec.std_batch, style_title)
                    worksheet.write_merge(row,row,44,45,rec.std_term, style_title)
                    worksheet.write_merge(row,row,46,50,rec.std_address, style_title)
                    worksheet.write_merge(row,row,51,52,rec.std_gender, style_title)
                    worksheet.write_merge(row,row,53,54,rec.adm_date, style_title)
                    worksheet.write_merge(row,row,55,59,rec.waiver_1, style_title)
                    worksheet.write_merge(row,row,60,64,rec.waiver_2, style_title)

   
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
        

   
                

           

























