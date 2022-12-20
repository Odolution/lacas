# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'User Wise Invoices',
    'version': '1.0.0',
    'category': 'Accounting',
    'summary': 'User Wise Invoices',
    'description': """
        This is a custom module , User Wise Invoices, Lacas custom requirements to filterout domains of a school.
    """,
    'depends': ['account'],    
    'data': [
        # the order matters here
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/account_view.xml",
        "views/user_view.xml",
    ],
    'demo': [],
    "application":True,
    'auto_install': False,
    "sequence":-100,
    "licence":"LGPL-3",
    'assets': {
    },
}


# <record id="view_account_move_form" model="ir.ui.view">
#         <field name="name">account.move.form</field>
#         <field name="model">account.move</field>
#         <field name="inherit_id" ref="account.view_move_form"/>
#         <field name="arch" type="xml">
#             <xpath expr="//div[@name='journal_div']" position="after">
#                 <field name="student_name"/>
#                 <field name="student_id"/>
#             </xpath>
#         </field>
#     </record>