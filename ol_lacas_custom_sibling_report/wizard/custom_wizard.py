
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
                for students in rec.student_ids:
                    roll_no=students.facts_udid
                    name=students.name
                    phone=students.phone
                    street=students.street
                    # branch=students.school_ids.name
                    batch=students.x_studio_btachsesson 
                    classs=students.homeroom
                    gender=students.gender
                    if students.enrollment_state_ids:
                        for line in students.enrollment_state_ids:
                            enroll_dt=line.enrolled_date
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
                            fcraw_dis=plans.x_studio_fc_row
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
                "parent_code":'',
                "father_name":f_name if f_name else 'No Father Name',
                "f_phone_no":f_ph  if f_name else phone,
                "f_cnic":'',
                "f_address":f_st  if f_st else 'No Father Address',
                "std_address":street  if street else 'No Std Address',
                "no_of_child":tot_child,
                "m_cnic":"",
                "mother_name":m_name  if m_name else 'No Mother Name',
                "m_phone_no":m_ph  if f_ph else 'No Moth phone',
                "emergency":'',
                "std_name":name,
                "std_gender":gender if gender else "Not Assigned",
                "adm_date":enroll_dt ,
                "std_branch":branch,
                "std_batch":batch if batch else "Empty batch",
                "std_term":"",
                "std_class":classs if classs else "Not assigned class",
                "waiver_1":all_dis if all_dis else 'No Discount',
                "waiver_2":fcraw_dis if fcraw_dis else 'No fcraw Disc',
                        

        })
            lines.append(mvl.id)
            lst=[]
            lst.append(mvl.roll_no)
            lst.append(mvl.parent_code)
            lst.append(mvl.father_name)
            lst.append(mvl.f_phone_no)
            lst.append(mvl.f_address)
            lst.append(mvl.std_address)
            lst.append(mvl.no_of_child)
            lst.append(mvl.mother_name)
            lst.append(mvl.adm_date)
            lst.append(mvl.std_class)
            raise UserError(lst)

                        
        
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
            worksheet.write_merge(0, 1, 6, 11, "SIBLING STUDENTS REPORT", style=style_title)
            
            

    #         worksheet.write_merge(2,3,0,0,"Sr.No", style=red_style_title)
    #         worksheet.write_merge(2,3,1,3,"ID",style=red_style_title)
    #         worksheet.write_merge(2,3,4,5,"App Date",style=red_style_title)
    #         worksheet.write_merge(2,3,6,7,"Roll No",style=red_style_title)
    #         worksheet.write_merge(2,3,8,9,"6 Digit Roll No",style=yellow_style_title)
    #         worksheet.write_merge(2,3,10,11,"Name",style=red_style_title)
    #         worksheet.write_merge(2,3,12,13,"Batch #",style=red_style_title)
    #         worksheet.write_merge(2,3,14,16,"Branch",style=red_style_title)
    #         worksheet.write_merge(2,3,17,18,"Class",style=red_style_title)
    #         worksheet.write_merge(2,3,19,20,"withdrawn Status", red_style_title)
    #         worksheet.write_merge(2,3,21,22,"Leaving Reaon", red_style_title)
    #         worksheet.write_merge(2,3,23,24,"Remarks", red_style_title)
    #         worksheet.write_merge(2,3,25,26,"Withdrawn DT", red_style_title)


    #         v_from_month=datetime.strptime(str(self.date_from), "%Y-%m-%d").strftime('%m')
    #         v_from_year=datetime.strptime(str(self.date_from), "%Y-%m-%d").strftime('%y')

    #         v_to_month=datetime.strptime(str(self.date_to), "%Y-%m-%d").strftime('%m')
    #         v_to_year=datetime.strptime(str(self.date_to), "%Y-%m-%d").strftime('%y')

    #         months= {
    #             1:['01','JAN-22',10,'22'],
    #             2:['02','FEB-22',20,'22'],
    #             3:['03','MAR-22',30,'22'],
    #             4:['04','APR-22',40,'22'],
    #             5:['05','MAY-22',50,'22'],
    #             6:['06','JUN-22',60,'22'],
    #             7:['07','JUL-22',70,'22'],
    #             8:['08','AUG-22',80,'22'],
    #             9:['09','SEP-22',90,'22'],
    #             10:['10','OCT-22',100,'22'],
    #             11:['11','NOV-22',110,'22'],
    #             12:['12','DEC-22',120,'22'],
    #             13:['01','JAN-23',130,'23'],
    #             14:['02','FEB-23',140,'23'],
    #             15:['03','MAR-23',150,'23'],
    #             16:['04','APR-23',160,'23'],
    #             17:['05','MAY-23',170,'23'],
    #             18:['06','JUN-23',180,'23'],
    #             19:['07','JUL-23',190,'23'],
    #             20:['08','AUG-23',200,'23'],
    #             21:['09','SEP-23',200,'23'],
    #             22:['10','OCT-23',200,'23'],
    #             23:['11','NOV-23',200,'23'],
    #             24:['12','DEC-23',200,'23'],
    #             }
    #         range_start = 0
    #         range_stop = 0
    #         # raise UserError(v_to)
    #         for key, value in months.items():
    #             if value[0] == v_from_month and value[3] == v_from_year:
    #                 range_start = key
    #             if value[0] == v_to_month and value[3] == v_to_year:

    #                 range_stop = key

    #         col = 27
            
      
    #         for i in range(range_start,range_stop+1):
      
    #             worksheet.write_merge(2,3,col,col+1,months[i][1],red_style_title)
    #             # worksheet.write_merge(row,row,col,col+1,months[i][2])
    #             col+=2

    #         worksheet.write_merge(2,3,col,col+1,"Total", lime_style_title)   
            
    #             # print('col:',months[i][1], 'data:',months[i][2])

    #         # row = 4
    #         # sno = 1
        
    #         column = 27
    #         row = 4
    #         sn=1
    #         for rec in self.account_report_line:
                

                
    #             if rec:

    #                 column = 27

    #                 worksheet.write(row,0,sn)
    #                 worksheet.write_merge(row,row,1,3,rec.record_id,heading_style)
    #                 worksheet.write_merge(row,row,4,5,rec.app_date,heading_style)
    #                 worksheet.write_merge(row,row,6,7,rec.roll_no,heading_style)
    #                 worksheet.write_merge(row,row,8,9,rec.full_roll_no,heading_style)
    #                 worksheet.write_merge(row,row,10,11,rec.name,heading_style)
    #                 worksheet.write_merge(row,row,12,13,rec.student_batch,heading_style)
    #                 worksheet.write_merge(row,row,14,16,rec.student_branch,heading_style)
    #                 worksheet.write_merge(row,row,17,18,rec.student_class,heading_style)
    #                 worksheet.write_merge(row,row,19,20,rec.withdrawn_status,heading_style)
    #                 worksheet.write_merge(row,row,21,22,rec.leaving_reason,heading_style)
    #                 worksheet.write_merge(row,row,23,24,rec.remarks,heading_style)
    #                 worksheet.write_merge(row,row,25,26,rec.withdrawn_date,heading_style)

    #                 data_month= {
    #                     1:['01','JAN-22',rec.jan,'22'],
    #                     2:['02','FEB-22',rec.feb,'22'],
    #                     3:['03','MAR-22',rec.mar,'22'],
    #                     4:['04','APR-22',rec.apr,'22'],
    #                     5:['05','MAY-22',rec.may,'22'],
    #                     6:['06','JUN-22',rec.jun,'22'],
    #                     7:['07','JUL-22',rec.jul,'22'],
    #                     8:['08','AUG-22',rec.aug,'22'],
    #                     9:['09','SEP-22',rec.sep,'22'],
    #                     10:['10','OCT-22',rec.oct,'22'],
    #                     11:['11','NOV-22',rec.nov,'22'],
    #                     12:['12','DEC-22',rec.dec,'22'],
    #                     13:['01','JAN-23',rec.jan_2,'23'],
    #                     14:['02','FEB-23',rec.feb_2,'23'],
    #                     15:['03','MAR-23',rec.mar_2,'23'],
    #                     16:['04','APR-23',rec.apr_2,'23'],
    #                     17:['05','MAY-23',rec.may_2,'23'],
    #                     18:['06','JUN-23',rec.jun_2,'23'],
    #                     19:['07','JUL-23',rec.jul_2,'23'],
    #                     20:['08','AUG-23',rec.aug_2,'23'],
    #                     21:['09','SEP-23',rec.sep_2,'23'],
    #                     22:['10','OCT-23',rec.oct_2,'23'],
    #                     23:['11','NOV-23',rec.nov_2,'23'],
    #                     24:['12','DEC-23',rec.dec_2,'23'],
    #                 }
    #                 range_start = 0
    #                 range_stop = 0
                  
    #                 for key, value in data_month.items():
    #                     if value[0] == v_from_month and value[3] == v_from_year:
    #                         range_start = key
    #                     if value[0] == v_to_month and value[3] == v_to_year:
    #                         range_stop = key
                    

    #                 for i in range(range_start,range_stop+1):
    #                     # raise UserError(column)
    #                     worksheet.write_merge(row,row,column,column+1,data_month[i][2],heading_style)
    #                     # worksheet.write_merge(row,row,column,column+1,rec.total_amount)
    #                     # lst.append([row_1,row_1,column,column+1])
                      
    #                     column+=2
    #                 worksheet.write_merge(row,row,column,column+1,rec.total_amount,heading_style)
                      
    #                 row+=1
    #                 sn+=1

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
        

   
                

           

























