# -*- coding: utf-8 -*-


{
    'name': 'Lacas One Child report',

    "author": "Nadia | Odolution",
    'version': '0.1',
    'category': 'Invoice Customization',
    'sequence': -99,
    'summary': 'Report of Students with no onechild in lacas',
    'description': "",
    'website': '',
    'images': [
    ],
    'depends': ["account","base",
    ],
    'data': [
        
        # "views/view.xml",
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
