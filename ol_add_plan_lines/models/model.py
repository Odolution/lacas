
from odoo import models, api, fields, _
from odoo.exceptions import UserError
import json
import datetime



class add_plan_line_wiz(models.TransientModel):
    _name='tuition.add_plan_line_wiz'
    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    product_id = fields.Many2one('product.product', string='Product')
    installment_names=fields.Many2many('installment.name',string="Billing Cycle")
    
    unit_price=fields.Integer("Unit Price")
    currency_id=fields.Many2one('res.currency',"Currency")
    quantity = fields.Integer("Quantity")
    
    operation=fields.Selection([('add','Add'),('update','Update')],"Operation")
    def apply(self):
        if self.operation=="add":
            val=""
            lis1t=[]
            list2=[]
            for t_plan in self.plan_ids:
                for p in t_plan.line_ids:
                    if p.product_id==self.product_id:
                        lis1t.append(t_plan)
                        val="yes"
            if lis1t:
                for li in lis1t:
                    udid=li.student_id.facts_udid
                    name= li.student_id.name
                    stu=str(udid)+" "+ name+ " "
                    list2.append(stu)
                raise UserError("Charge is Already Exist in the following students: "+str(list2)[1:-1])
            else:
                self.add()
            # for t_plan in self.plan_ids:
            #     for p_lines in t_plan.line_ids:
            #         val=""
            #         if p_lines.product_id == self.product_id:
            #             #raise UserError("already exist in plan")
            #             val="yes"
            #         else:
            #             val="no"
            # if val=="yes":
            #     raise UserError("Charge is already exist in Tuition Plan!!")
            # else:
            #     self.add()
        else:
            self.update()
    def add(self):
            lst=[]
            lst_fc=[]
            for plan in self.plan_ids:
                        names=[i.name for i in self.installment_names]
                        installment_ids=self.env['tuition.installment'].search([
                                        ('name','in',names),
                                        ('tuition_plan_id','=',plan.id)])
                        #if discounted product then add discount name and value 
                        if self.product_id.is_discount_type:
                             #fcraw discounted values 
                            if self.product_id.x_studio_is_fcraw:
                                tuition_plan=self.env['tuition.plan'].search([('id','=',plan.id)])
                                lst_fc.append(self.product_id.name)
                                tuition_plan["x_studio_fcraw_name"]=' |  '.join(lst_fc)
                                valst_fc=[]
                                total_fc=[]
                                length=len(self.product_id.discount_ids)
                                sum=0
                                for dis in self.product_id.discount_ids:
                                    # length=len(dis)
                                    val=int(dis.discount_value)
                                    sum=val+sum
                                    if length!=0:
                                        div=sum/length
                                        valst_fc.append(div)
                                total_fc = 0
                                for num in valst_fc:
                                    total_fc += num
                                t=int(total_fc)
                                tot=str(t)
                                if tot!='0':
                                    tuition_plan["x_studio_fcraw_value"]=tot
                                else:
                                    tuition_plan["x_studio_fcraw_value"]=''
                                if self.unit_price==0:
                                    tuition_plan["x_studio_fcraw"]=0
                                if self.unit_price>0:
                                    tuition_plan["x_studio_fcraw"]=1
                            else:
                                tuition_plan=self.env['tuition.plan'].search([('id','=',plan.id)])
                                if self.unit_price==0:
                                    tuition_plan["x_studio_have_discount_1"]=0
                                if self.unit_price>0:
                                    tuition_plan["x_studio_have_discount_1"]=1
                                if not self.product_id.x_studio_is_fcraw:
                                    lst.append(self.product_id.name)
                                    tuition_plan["x_studio_discount_name_1"]=' |  '.join(lst)
                                    valst=[]
                                    total=[]
                                    length=len(self.product_id.discount_ids)
                                    sum=0
                                    for dis in self.product_id.discount_ids:
                                        if length!=0:
                                        # length=len(dis)
                                            val=int(dis.discount_value)
                                            sum=val+sum
                                    div=sum/length
                                    valst.append(div)
                                    total = 0
                                    for num in valst:
                                        total += num
                                    t=int(total)
                                    tot=str(t)
                                    if tot!='0':
                                        tuition_plan["x_studio_discount_value_1"]=tot
                                    else:
                                        tuition_plan["x_studio_discount_value_1"]="0"
                            
                        
                        linedata={
                                    'plan_id':plan.id,
                                    'product_id':self.product_id.id,
                                    'name':self.product_id.name,
                                    'account_id':self.product_id.property_account_income_id.id,
                                    'quantity':self.quantity,
                                    'installment_ids':[(6,0,[i.id for i in installment_ids if i.name in names])],
                                    'currency_id':self.currency_id.id,
                                    'unit_price':self.unit_price
                                    }
                        new_plan_line_id=self.env['tuition.plan.line'].create(linedata)

    def update(self):
            for plan in self.plan_ids:
                        names=[i.name for i in self.installment_names]
                        installment_ids=self.env['tuition.installment'].search([
                                        ('name','in',names),
                                        ('tuition_plan_id','=',plan.id)])
                        if self.product_id.is_discount_type:
                            if self.product_id.x_studio_is_fcraw:
                                tuition_plan=self.env['tuition.plan'].search([('id','=',plan.id)])
                                if self.unit_price==0:
                                    tuition_plan["x_studio_fcraw"]=0
                                if self.unit_price>0:
                                    tuition_plan["x_studio_fcraw"]=1
                            else:
                                tuition_plan=self.env['tuition.plan'].search([('id','=',plan.id)])
                                if self.unit_price==0:
                                    tuition_plan["x_studio_have_discount_1"]=0
                                if self.unit_price>0:
                                    tuition_plan["x_studio_have_discount_1"]=1
                        
                        linedata={
                                    'plan_id':plan.id,
                                    'product_id':self.product_id.id,
                                    'name':self.product_id.name,
                                    'account_id':self.product_id.property_account_income_id.id,
                                    'quantity':self.quantity,
                                    'installment_ids':[(6,0,[i.id for i in installment_ids if i.name in names])],
                                    'currency_id':self.currency_id.id,
                                    'unit_price':self.unit_price
                                    }
                        line=self.env['tuition.plan.line'].search([('plan_id',"=",plan.id),('product_id',"=",self.product_id.id)])
                        line.write(linedata)


    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        ids=self._context.get("active_ids")
        res["plan_ids"]=[(6,0,ids)]
        return res
    
class set_next_installment_wiz(models.TransientModel):
    _name='tuition.set_next_installment_wiz'
    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    installment_name=fields.Many2one('installment.name',string="Billing Cycle")
    
    def apply(self):
        for plan in self.plan_ids:
                        
            installment_ids=self.env['tuition.installment'].search([
                                        ('name','in',self.installment_name.name),
                                        ('tuition_plan_id','=',plan.id)])
            for installment_id in installment_ids:
                if installment_id.name==self.installment_name.name:
                    plan.next_installment_id=installment_id.id     
                        
    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        ids=self._context.get("active_ids")
        res["plan_ids"]=[(6,0,ids)]
        return res
class installment_names(models.Model):

    _name = "installment.name"
    name = fields.Char(string='Name')
