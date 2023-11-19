from odoo import models, api, fields
from odoo.exceptions import UserError
import json
import datetime
import calendar



# class wizard_tuition_plan(models.TransientModel):
#     _name='tuition.wizard_tuition_plan'

#     plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
#     tuition_template_id = fields.Many2one('tuition.template', string='Tuition Template')

    
#     def apply(self):
        
#         tuition_lines=self.tuition_template_id.line_ids

#         for t_plan in self.plan_ids:
#             # onchange function
#             if self.tuition_template_id:
#                 t_plan.tuition_template_id=self.tuition_template_id

#             for lines in t_plan.line_ids:
#                 for line in tuition_lines:
#                     if lines.product_id==line.product_id:
#                         continue
#                         if lines.unit_price!=line.unit_price:
#                             lines.unit_price=line.unit_price
#                     else:
#                         # t_plan= self.env['tuition.plan'].browse(t_plan.id)
#                         new_line = self.env['tuition.plan.line'].new({
#                                 'product_id': line.product_id,
#                                 'plan_id': t_plan.id,
#                                 'currency_id':1,
#                                 'name':line.name,
#                                 # Add other field values as needed
#                             })
#                         t_plan.line_ids += new_line


class wizard_tuition_plan(models.TransientModel):
    _name = 'tuition.wizard_tuition_plan'

    plan_ids = fields.Many2many('tuition.plan', string='tuition_plan')
    tuition_template_id = fields.Many2one('tuition.template', string='Tuition Template')

    def apply(self):
        tuition_lines = self.tuition_template_id.line_ids

        price = {}
        for line in self.tuition_template_id.line_ids:
            price[line.name] = line.unit_price

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        installment_ids = self.env['tuition.installment'].search([('month', 'in', months)])
        installment_ids = installment_ids.ids


        for t_plan in self.plan_ids:
             # onchange function
            # if self.tuition_template_id:
            t_plan.tuition_template_id=self.tuition_template_id

            # if t_plan.student_grade_level_ids.name == "XI":
            #     # raise UserError(t_plan.student_grade_level_ids.name)
            #     # specialization_charges_remove = t_plan.line_ids.filtered(lambda l2: l2.product_id.x_studio_code and l2.product_id.x_studio_code.strip())
            #     specialization_charges_remove = t_plan.line_ids.filtered(lambda l2: l2.product_id.x_studio_code in ['ART', 'BIO', 'CHM', 'COM', 'PHY'])
            #     # raise UserError(specialization_charges_remove.product_id.name)
            #     specialization_charges_remove.unlink()

            

            if t_plan.student_grade_level_ids.name == "XI":
                #lines_to_remove = t_plan.line_ids.filtered(lambda l: l.product_id.x_studio_code in ['ART', 'BIO', 'CHM', 'COM', 'PHY'] or l.product_id.is_discount_type == 0)
                lines_to_override = t_plan.line_ids.filtered(lambda l: not (l.product_id.x_studio_code or l.product_id.is_discount_type))
                lines_to_override.unlink()
            else:
                non_discount_lines_to_remove =t_plan.line_ids.filtered(lambda l: l.product_id.x_studio_code not in ['ART', 'BIO', 'CHM', 'COM', 'PHY']  and l.product_id.is_discount_type == 0)
                non_discount_lines_to_remove.unlink()

                # raise UserError("do not unlink")

            # if t_plan.student_grade_level_ids.name == "XI":
            #     for line in t_plan.line_ids:
            #         # raise UserError(line)
            #         if line.product_id.x_studio_code in ['ART', 'BIO', 'CHM', 'COM', 'PHY']:
            #             line.unlink()

            
            for line in tuition_lines:
            
                existing_line = t_plan.line_ids.filtered(lambda l: l.product_id == line.product_id)
                if existing_line:
                    if existing_line.unit_price != line.unit_price:
                        existing_line.unit_price = line.unit_price
                else:
                    # price = price_dct.get(line.name)
                    # if not price:
                    #     line.product_id.list_price
                    
                    new_line = self.env['tuition.plan.line'].create({
                        'product_id': line.product_id.id,
                        'plan_id': t_plan.id,
                        'currency_id': 1,
                        'name': line.name,
                        'quantity': line.quantity,
                        # 'discount': line.discount,
                        'unit_price': price.get(line.name),
                        # 'installment_ids':t_plan.installment,

                        'installment_ids':t_plan.installment_ids,
                        
                        # 'installment_ids':t_plan.installment,
                        # 'installment_ids': installment.get(line.name),


                        'account_id': line.product_id.property_account_income_id.id,
                        # 'account_id': line.account_id.id,
                        # Add other field values as needed

                        
                    })
                    # added_product_ids.add(line.product_id.id)

    def default_get(self, fields_list):
        # OVERRIDE
        res = super().default_get(fields_list)
        ids=self._context.get("active_ids")
        res["plan_ids"]=[(6,0,ids)]
        return res
