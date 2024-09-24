# -*- coding: utf-8 -*-
{
    'name': "OL - School management",

    'version': '0.27',

    'depends': [
        'base',
        'portal',
        'contacts',
        'hr_skills',
        'calendar',
        # 'ol_school_manager',
        # 'ol_school_account',
        ],

    'data': [

        # Wizards
        'wizards/ol_migration_tool_view.xml',
        'wizards/ol_main_wizard/ol_main_wizard_view.xml',
        
        # Security
        
        'security/secure_relationship_rule.xml',
        'security/ir.model.access.csv',
        
        # Records

        'data/ol_update.xml',
        'data/ol_no_update.xml',
        'views/ol_main_views.xml',

        # Views
        'views/ol_inherit/ol_inherit_res_users.xml',
        'views/ol_settings/ol_structure_school.xml',
        'data/ol_datamenu.xml',

        
        ],


    'application': True,

    'assets': {
        'web.assets_qweb': [
            'ol_school_manager/static/src/xml/views.xml'
            ],
        'web.assets_backend': [
            
            'ol_school_manager/static/src/webclient/**/*',


            'ol_school_manager/static/src/js/backend/*',
            'ol_school_manager/static/src/scss/*',

            # Libs
            'ol_school_manager/static/lib/jstree/dist/jstree.js',
            'ol_school_manager/static/lib/jstree/dist/themes/default/style.css',
            ],
        'web.assets_common': [
            'ol_school_manager/static/src/js/common/*',
            ],

        'web.tests_assets': [
            'ol_school_manager/static/tests/switch_school_menu.js'
            ],
    },

    'license': 'OPL-1',
}
