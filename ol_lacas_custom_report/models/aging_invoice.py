
from odoo import models, api, fields, _
# from odoo.exceptions import UserError
from datetime import datetime
import xlsxwriter

# from ast import dump
# from collections import UserString
# from dataclasses import field
# from email.policy import default
# from itertools import product
# import json
# # from odoo import models, api, fields, _
# from odoo.tools import date_utils
# from odoo.exceptions import UserError
# from datetime import datetime
# import xlsxwriter

# import time
# import json
# import datetime
# import io
# from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
# from odoo.tools import date_utils
# try:
    # from odoo.tools.misc import xlsxwriter
# except ImportError:
    # import xlsxwriter


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


class AccountMoveAging(models.Model):
    _name = 'aging.invoice.line'

    customer_name   =   fields.Char('Customer Name')
    region_name     =   fields.Char('Region')
    area            =   fields.Char('Area')
    contact_num     =   fields.Char('Contact Number')
    invoice_date    =   fields.Date('Invoice Date')
    invoice_num     =   fields.Char('Invoice Number')
    invoice_amount  =   fields.Float('Amount')
    received_amount =   fields.Float('Received')
    balance_amount  =   fields.Float('Balance Amount')
    due_date        =   fields.Date('Due Date')
    days_due        =   fields.Integer('Due Days')
    # total_amount    =   fields.Float("Total Amount")
    heading         =   fields.Char('Heading')



class AgingInvoice(models.Model):
    _name = 'aging.invoice'

    start_date = fields.Date('Date From')
    end_date = fields.Date('Date To')

    invoice_date = fields.Date('Invoice Date')
    due_date = fields.Date('Due Date')

    sale_person_filter = fields.Many2many('res.users', string='Sale Person')
    customer_filter = fields.Many2many('res.partner', string='Customer')

    region_filter = fields.Many2many('region.region', string='Region')
    subregion_filter = fields.Many2many('town.town', string='Sub Region')
    area_filter = fields.Many2many('account.account', string='Area')

    aging_invoice_ids = fields.Many2many('aging.invoice.line', string='Aging Wise Invoice')

    groups_ids = fields.Many2many('aging.invoice.group', string='Groups')

    @api.onchange('area_filter')
    def area_filter_onchange(self):

        return {'domain': {'area_filter': [('internal_type', '=', 'receivable')]}}
    
    def get_grp_field_value_from_obj(self,grp,obj):
            grpfields=grp.split(".")
            output=obj
            for grpfield in grpfields:
                    
                    output=output[grpfield]
            return output
    
    def recursiveGetData(self,data,appendablelist):
        locallist=[]
        
                
        for key in data.keys():
            val=data[key]
            appendablelist.append({
                    "heading":"Group: "+str(key),
                    })
            if type(val)==type(dict()):
                val = self.recursiveGetData(val,appendablelist)

            elif type(val)==type(list()):
                for value in val:
                    receivable_amount = 0
                    for payment_val in value._get_reconciled_info_JSON_values():
                        receivable_amount += payment_val['amount']

                    if self.end_date and value.invoice_date_due:
                        d1 = datetime.strptime(str(self.end_date), "%Y-%m-%d")
                        d2 = datetime.strptime(str(value.invoice_date_due), "%Y-%m-%d")
                        delta = d1 - d2

                        appendablelist.append({
                        "customer_name":value.partner_id.name,
                        "region_name":value.partner_id.region_id.name,
                        "area":value.partner_id.property_account_receivable_id.name,
                        "contact_num":value.partner_id.phone,
                        "invoice_date":value.invoice_date,
                        "invoice_num":value.name,
                        "invoice_amount":value.amount_total,
                        "received_amount":receivable_amount,
                        "balance_amount":value.amount_residual,
                        "due_date":value.invoice_date_due,
                        "days_due":delta.days,
                        })

                    else:
                        appendablelist.append({
                            "customer_name":value.partner_id.name,
                            "region_name":value.partner_id.region_id.name,
                            "area":value.partner_id.property_account_receivable_id.name,
                            "contact_num":value.partner_id.phone,
                            "invoice_date":value.invoice_date,
                            "invoice_num":value.name,
                            "invoice_amount":value.amount_total,
                            "received_amount":receivable_amount,
                            "balance_amount":value.amount_residual,
                            "due_date":value.invoice_date_due,
                            # "days_due":delta.days,
                            })
                
            else:
                print("invalid datatype ")
                # print(val)
                # return
            amount_total=0
            bal_amount = 0
            receive_amount = 0
            
            for value in val:
                locallist.append(value)
                amount_total+=value.amount_total
                bal_amount+=value.amount_residual

                receivable_amount = 0
                for payment_val in value._get_reconciled_info_JSON_values():
                    receivable_amount += payment_val['amount']

                receive_amount+=receivable_amount

            appendablelist.append({
                    "invoice_num":str(key)+" total",
                    "invoice_amount":amount_total,
                    "received_amount":receive_amount,
                    "balance_amount":bal_amount,
                    })

        return locallist


    def get_invoices(self):

        # raise UserError(str(datetime.now().date()))
        #delete all records first

        record_set = self.env['aging.invoice.line'].search([])
        record_set.unlink()

        #creating dynamic filters
        filter_list = [("move_type","=","out_invoice")]

        if self.invoice_date:
            filter_list.append(("invoice_date","=",self.invoice_date))

        if self.due_date:
            filter_list.append(("invoice_date_due","=",self.due_date))

        if self.start_date:
            # filter_list.append("|")
            filter_list.append(("invoice_date",">=",self.start_date))

        if self.end_date:
            filter_list.append(("invoice_date","<=",self.end_date))
        
        if self.customer_filter:
            if len(self.customer_filter) > 1:

                customer_list = []
                for cust in self.customer_filter:
                    customer_list.append(cust.id)
                filter_list.append(("partner_id.id","in",customer_list))
                
            else:
                filter_list.append(("partner_id.id","=",self.customer_filter.id))
        
        if self.sale_person_filter:
            if len(self.sale_person_filter) > 1:

                saleperson_list = []
                for sale in self.sale_person_filter:
                    saleperson_list.append(sale.id)
                filter_list.append(("invoice_user_id.id","in",saleperson_list))
                
            else:
                filter_list.append(("invoice_user_id.id","=",self.sale_person_filter.id))

        if self.region_filter:
            if len(self.region_filter) > 1:

                region_list = []
                for reg in self.region_filter:
                    region_list.append(reg.id)
                filter_list.append(("partner_id.region_id.id","in",region_list))
                
            else:
                filter_list.append(("partner_id.region_id.id","=",self.region_filter.id))
        
        if self.subregion_filter:
            if len(self.subregion_filter) > 1:

                subregion_list = []
                for subreg in self.subregion_filter:
                    subregion_list.append(subreg.id)
                filter_list.append(("partner_id.town_id.id","in",subregion_list))
                
            else:
                filter_list.append(("partner_id.town_id.id","=",self.subregion_filter.id))

        if self.area_filter:
            if len(self.area_filter) > 1:

                area_list = []
                for area in self.area_filter:
                    area_list.append(area.id)
                filter_list.append(("partner_id.property_account_receivable_id.id","in",area_list))
                
            else:
                filter_list.append(("partner_id.property_account_receivable_id.id","=",self.area_filter.id))
        # raise UserError(str(filter_list))

        if not self.end_date:
            self.end_date = str(datetime.now().date())
        # get data from acount.move

        move_ids = self.env['account.move'].search(filter_list)

        # #grouping logic

        if self.groups_ids:

            dict_data={}
            for mov in move_ids:
                data=dict_data
                group_lst = []
                for grp in self.groups_ids:
                    ans=self.get_grp_field_value_from_obj(grp.grouping,mov)
                    group_lst.append(ans)


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

            # raise UserError(str(dict_data))

            datalist=[]                                             ##this list hold objects that need to be created
            final_list=self.recursiveGetData(dict_data,datalist)         #this list holds items for final sum
            # creating line in aging.invoice.line
            lines=[]
            for data in datalist:

                mvl=self.env['aging.invoice.line'].create(data)
                lines.append(mvl.id)

        # creating line without grouping
        else:
            lines=[]       
            for mv in move_ids:

                # get payment value againt invoice
                receivable_amount = 0
                for payment_val in mv._get_reconciled_info_JSON_values():
                    receivable_amount += payment_val['amount']

                if self.end_date and mv.invoice_date_due:
                    d1 = datetime.strptime(str(self.end_date), "%Y-%m-%d")
                    d2 = datetime.strptime(str(mv.invoice_date_due), "%Y-%m-%d")
                    delta = d1 - d2

                    # creating line in aging.invoice.line
                    mvl=self.env['aging.invoice.line'].create({
                    "customer_name":mv.partner_id.name,
                    "region_name":mv.partner_id.region_id.name,
                    "area":mv.partner_id.property_account_receivable_id.name,
                    "contact_num":mv.partner_id.phone,
                    "invoice_date":mv.invoice_date,
                    "invoice_num":mv.name,
                    "invoice_amount":mv.amount_total,
                    "received_amount":receivable_amount,
                    "balance_amount":mv.amount_residual,
                    "due_date":mv.invoice_date_due,
                    "days_due":delta.days,
                    })

                        

                else:
                    
                    # creating line in aging.invoice.line
                    mvl=self.env['aging.invoice.line'].create({
                    "customer_name":mv.partner_id.name,
                    "region_name":mv.partner_id.region_id.name,
                    "area":mv.partner_id.property_account_receivable_id.name,
                    "contact_num":mv.partner_id.phone,
                    "invoice_date":mv.invoice_date,
                    "invoice_num":mv.name,
                    "invoice_amount":mv.amount_total,
                    "received_amount":receivable_amount,
                    "balance_amount":mv.amount_residual,
                    "due_date":mv.invoice_date_due,
                    # "days_due":delta.days,
                    })

                # creating line in aging.invoice.line
                # mvl=self.env['aging.invoice.line'].create({
                #     "customer_name":mv.partner_id.name,
                #     "region_name":mv.partner_id.region_id.name,
                #     "area":mv.partner_id.property_account_receivable_id.name,
                #     "contact_num":mv.partner_id.phone,
                #     "invoice_date":mv.invoice_date,
                #     "invoice_num":mv.name,
                #     "invoice_amount":mv.amount_total,
                #     "received_amount":receivable_amount,
                #     "balance_amount":mv.amount_residual,
                #     "due_date":mv.invoice_date_due,
                #     # "days_due":mv.partner_id.region_id.name,
                #     })
                
                lines.append(mvl.id)

        #update records in many2many field   
        self.write({
            "aging_invoice_ids":[(6,0,lines)]
        })

    def print_xlsx(self):

        # raise UserError("check")

        # datalines=[]
        # for rec in self.aging_invoice_ids:
        #     datalines.append([rec.heading,rec.customer_name,rec.region_name,rec.area,rec.contact_num,rec.invoice_date,rec.invoice_num,rec.invoice_amount,rec.received_amount,rec.balance_amount,rec.due_date,rec.days_due,rec.heading])
        # datafields=["Customer Name","Town","Area","Contact #","Invoice Date","Invoice #","Amount","Received","Balance","Due Date","Due Days"]
        
        # salespersonlist = []
        # customerlist = []

        # for i in self.sale_person_filter:
        #     salespersonlist.append(i.name)
        # for j in self.customer_filter:
        #     customerlist.append(j.name)

        # data={
        #     "model_id":self.id,
        #     "datalines":datalines,  
        #     "start_date":self.start_date,
        #     "end_date":self.end_date,
        #     "saleperson":salespersonlist,
        #     "customer":customerlist,

        #     }

        # return self.env.ref('aging_receivable_report_invoice.receivable_xlsx').report_action(self, data=data)

        if xlwt:

            
            salespersonlist = []
            customerlist = []

            for i in self.sale_person_filter:
                salespersonlist.append(i.name)
            for j in self.customer_filter:
                customerlist.append(j.name)

            
            filename = 'Aging Invoice wise.xls'
            # One sheet by partner
            workbook = xlwt.Workbook()
            # sheet = workbook.add_sheet(report_name[:31])
            worksheet = workbook.add_sheet('Aging Invoice wise')
            

            
            style_title = xlwt.easyxf(
            "font:bold on,; align: vertical center,horiz center; border: top thin, bottom thin, right thin, left thin")

            grand_heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True;')

            heading_style = xlwt.easyxf('pattern: pattern solid, fore_colour black;'
                              'font: colour white, bold True;')
            
            date_format = xlwt.XFStyle()
            date_format.num_format_str = 'dd/mm/yyyy'

            worksheet.write_merge(0, 1, 0, 5,"HITECH OIL AND GHEE MILLS (PVT) LTD ",style=style_title)
            worksheet.write_merge(0, 1, 6, 11, "RECEIVABLE AGING INVOICES", style=style_title)
            worksheet.write_merge(0, 1, 12, 18,"AS ON "+"("+str(self.start_date)+")"+" - "+"("+str(self.end_date)+")", style=style_title)
            
            
            
            worksheet.write_merge(2,2,0,2,"Category: ",style=style_title)
            worksheet.write_merge(2,2,3,5,"Belt: ",style=style_title)
            # worksheet.write_merge(2,2,6,11,"SalePerson: " + str(salespersonlist),style=style_title)
            worksheet.write_merge(2,2,6,17,"Customer: " + str(customerlist),style=style_title)

            worksheet.write(3,0,"S#", style_title)
            worksheet.write_merge(3,3,1,3,"Customer Name",style=style_title)
            worksheet.write_merge(3,3,4,5,"Town",style=style_title)
            worksheet.write_merge(3,3,6,7,"Area",style=style_title)
            # worksheet.write(3,8,"Contact #", style_title)
            worksheet.write_merge(3,3,8,9,"Contact #",style=style_title)
            
            worksheet.write_merge(3,3,10,11,"Invoice Date",style=style_title)
            worksheet.write_merge(3,3,12,13,"Invoice #",style=style_title)
            
            worksheet.write(3,14,"Amount", style_title)
            worksheet.write(3,15,"Received", style_title)
            worksheet.write(3,16,"Balance", style_title)
            worksheet.write(3,17,"Due Date", style_title)
            worksheet.write(3,18,"Due Days", style_title)

            row = 4
            sno = 1
            
            for rec in self.aging_invoice_ids:

                if rec.heading:
                    worksheet.write_merge(row,row,1,3,rec.heading,grand_heading_style)

                elif not rec.heading and not rec.customer_name:
                    worksheet.write_merge(row,row,12,13,rec.invoice_num,heading_style)
                    worksheet.write(row,14,rec.invoice_amount,heading_style)
                    worksheet.write(row,15,rec.received_amount,heading_style)
                    worksheet.write(row,16,rec.balance_amount,heading_style)

                else:

                    worksheet.write(row,0,sno)
                    worksheet.write_merge(row,row,1,3,rec.customer_name)
                    worksheet.write_merge(row,row,4,5,rec.region_name)
                    worksheet.write_merge(row,row,6,7,rec.area)
                    # worksheet.write(3,8,"Contact #", style_title)
                    worksheet.write_merge(row,row,8,9,rec.contact_num)
                    
                    worksheet.write_merge(row,row,10,11,rec.invoice_date, date_format)
                    worksheet.write_merge(row,row,12,13,rec.invoice_num)
                    
                    worksheet.write(row,14,rec.invoice_amount)
                    worksheet.write(row,15,rec.received_amount)
                    worksheet.write(row,16,rec.balance_amount)
                    worksheet.write(row,17,rec.due_date, date_format)
                    worksheet.write(row,18,rec.days_due)

                    sno+=1
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
        

        

        
        
