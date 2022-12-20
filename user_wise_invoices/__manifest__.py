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
        "views/account_view.xml",
    ],
    'demo': [],
    "application":True,
    'auto_install': False,
    "sequence":-100,
    "licence":"LGPL-3",
    'assets': {
    },
}

