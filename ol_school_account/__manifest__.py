# -*- coding: utf-8 -*-
{
    'name': 'Ol - Finance Management',

    'category': 'Accounting',
    'version': '0.27',

    'depends': [
        'account',
        'sale',
        'base_automation',
        # 'ol_school_account',
        'ol_school_manager',
    ],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'wizards/ol_wizard_main_view.xml',
        

        'data/ol_base_data.xml',

        'views/ol_main_views.xml',
        
        

        
    ],

    'license': 'OPL-1',

    'assets': {
        'web.assets_qweb': [
            '/ol_school_account/static/src/xml/**/*.xml',
            '/ol_school_account/static/src/xml/fields.xml',
        ],
        'web.assets_backend': [
            '/ol_school_account/static/src/scss/backend/*.scss',
            '/ol_school_account/static/lib/js/pyeval.js',
            '/ol_school_account/static/src/js/backend/**/*.js',
        ]
    }
}
