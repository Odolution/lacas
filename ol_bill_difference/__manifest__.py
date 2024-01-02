# -*- coding: utf-8 -*-


{
    'name': 'Difference',

    "author": "Karimdad | Odolution",
    'category': 'Invoice Customization',
    'sequence': -101,
    'summary': 'Difference Calculation for lacas invoicing',
    'description': "Difference Calculation for lacas invoicing",
    'website': '',
    'depends': ["account", "challan_field"],
    'data': [
        "views/x_difference_view.xml",
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
