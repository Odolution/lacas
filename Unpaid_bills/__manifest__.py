# -*- coding: utf-8 -*-
{
    'name': "report",

    'description': """
        Unpaid Bills Report
    """,

    'author': "Osama Shaikh",
    'website': "http://www.odolution.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'report/reports.xml',
    ],

}
