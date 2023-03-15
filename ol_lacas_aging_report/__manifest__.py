# -*- coding: utf-8 -*-


{
    'name': 'Lacas Aging report',

    "author": "Nadia | Odolution",
    'version': '0.1',
    'category': 'Invoice Customization',
    'sequence': 95,
    'summary': 'Aging report wrt to receivables and recovery',
    'description': "",
    'website': '',
    'images': [
    ],
    'depends': ["account","base",
    ],
    'data': [
        
        "wizard/custom_wizard.xml",

        "security/ir.model.access.csv",

        

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
