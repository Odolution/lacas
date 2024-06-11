# -*- coding: utf-8 -*-
{
    'name': "Edoob Facts Integration",

    'summary': """
        Tool for the integration between school and facts""",

    'description': """
        Insert required field and views for avoid the sync with FACTS.
    """,

    'author': "Eduweb Group",
    'website': "https://www.eduwebgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Integration',
    'version': '0.8',

    # any module necessary for this one to work correctly
    'depends': [
        'edoob',
        'sincro_data_base',
        'edoob_finance',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',

        # data
        'data/menudata.xml',
        'data/actions.xml',
        'data/program_category.xml',

        # Settings
        'views/config_views.xml',

        # Views
        # People management
        'views/inherited/people_management/family_views.xml',
        'views/inherited/people_management/individual_views.xml',
        'views/inherited/people_management/student_views.xml',
        # School Structure
        'views/inherited/school_structure/school_structure_views.xml',
        
        'wizard/wizard.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'application': True,
}
