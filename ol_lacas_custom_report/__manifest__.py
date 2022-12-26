# -*- coding: utf-8 -*-


{
    'name': 'Lacas custom report',

    "author": "Nadia | Odolution",
    'version': '0.1',
    'category': 'Invoice Customization',
    'sequence': 95,
    'summary': 'Report of recieveables in  lacas account.move.',
    'description': "",
    'website': '',
    'images': [
    ],
    'depends': ["account","base"
    ],
    'data': [
        
        "views/view.xml",
        "wizard/custom_wizard.xml",
        "report/receivable_details.xml",
        "report/report_button.xml",
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
