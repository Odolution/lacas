
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

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
    _name = 'student.report.line'
    
    record_id=fields.Char('ID')
    branch_name=fields.Integer('Roll No')
    

class RecoveryReportWizard(models.TransientModel):
    _name="school.branch.report.wizard"
    _description='Print Recovery Wizard'

    
    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    
    account_report_line=fields.Many2many('student.report.line', string='Account report Line')


    
    def action_print_excel_school_branch_report(self):
        global first_date 
        global last_date
        

        # self.action_print_report()
        
        
        if xlwt:

            
            filename = 'RECEIVABLE OF WITHDRAWAL STUDENTS.xls'
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
            worksheet.write_merge(0, 1, 6, 11, "RECEIVABLE OF WITHDRAWAL STUDENTS", style=style_title)
            
            

            worksheet.write_merge(2,3,0,0,"Current Branch/School", style=red_style_title)
            worksheet.write_merge(2,3,1,3,"Billing month Jul-23",style=red_style_title)
            worksheet.write_merge(2,3,4,5,"App Date",style=red_style_title)
            worksheet.write_merge(2,3,6,7,"Branch Wise Recovery",style=red_style_title)
            worksheet.write_merge(2,3,8,9,"'%' age of Recovery",style=yellow_style_title)


            v_from_month=datetime.strptime(str(from_date), "%Y-%m-%d").strftime('%m')
            v_from_year=datetime.strptime(str(from_date), "%Y-%m-%d").strftime('%y')

            v_to_month=datetime.strptime(str(to_date), "%Y-%m-%d").strftime('%m')
            v_to_year=datetime.strptime(str(to_date), "%Y-%m-%d").strftime('%y')
            raise UserError(str(v_from_month)+" "+str(v_from_year)+" "+str(v_to_month)+" "+str(v_to_year))
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
                    worksheet.write_merge(row,row,4,5,rec.branch_name,heading_style)
                   

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
        