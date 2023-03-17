# -*- coding: utf-8 -*-


{
    'name': 'Lacas custom Accounting trees',

    "author": "Usama Shahid | Odolution",
    'version': '0.1',
    'category': 'Invoice Customization',
    'sequence': 95,
    'summary': 'Implementation different tree views of lacas account.move.',
    'description': "Implementation different tree views of lacas account.move.",
    'website': '',
    'images': [
    ],
    'depends': ["account",
    ],
    'data': [
        
        "views/view.xml",
        "views/tab_fields.xml",
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
    ],
    'license': 'LGPL-3',
}
