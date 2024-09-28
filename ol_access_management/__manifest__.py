# -*- coding: utf-8 -*-


{
    'name': 'Access Management',

    "author": "Developer | Odolution",
    'version': '0.1',
    'category': 'Manage Access',
    'sequence': 95,
    'summary': 'Manage access using rights',
    'description': "Manage access using rights",
    'website': '',
    'images': [
    ],
    'depends': ["base","ol_school_manager"],
    'data': [
        
        "views/view.xml",
        "security/ir.model.access.csv"
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
