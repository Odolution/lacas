# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Withdrawn Status Field',
    'author':'Maaz Ali',
    'version': '1.0',
    'category': '',
    'sequence':100,
    'summary': 'Create withdrawn status fields',
    'description': """""",
    'depends': ['account','cus_report'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        ],
    'demo': [],
    'installable': True,
    'assets': {},
    'application':True,
    'license': 'LGPL-3',
}
