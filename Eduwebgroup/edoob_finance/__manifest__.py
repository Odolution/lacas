# -*- coding: utf-8 -*-
{
    'name': 'Edoob - Finance Management',

    'summary': """ Edoob - Finance Management tools """,

    'description': """ Edoob - Finance Management added with gitlab """,

    'author': 'Eduweb Group',
    'website': 'https://www.eduwebgroup.com',

    'category': 'Accounting',
    'version': '0.27',

    'depends': [
        'account',
        'sale',
        'base_automation',
        'edoob',
    ],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'wizards/make_student_charge.xml',
        'wizards/create_bulk_tuition_plan.xml',
        'wizards/enroll_student_form.xml',
        'wizards/update_tuition_plan.xml',

        'data/mail_template_data.xml',
        'data/ir_actions_server_data.xml',

        'views/config_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',

        'views/school_finance_views.xml',
        'views/tuition_template_views.xml',
        'views/tuition_plan_views.xml',
        'views/school_family_individual_views.xml',
        'views/school_student_views.xml',
        'views/school_family_views.xml',

        'views/tuition_installment_views.xml',

        'data/ir_sequence.xml',
        'data/school_finance_data.xml',

        'data/menuitems.xml',
    ],

    'license': 'OPL-1',

    'assets': {
        'web.assets_qweb': [
            '/edoob_finance/static/src/xml/**/*.xml',
            '/edoob_finance/static/src/xml/fields.xml',
        ],
        'web.assets_backend': [
            '/edoob_finance/static/src/scss/backend/*.scss',
            '/edoob_finance/static/lib/js/pyeval.js',
            '/edoob_finance/static/src/js/backend/**/*.js',
        ]
    }
}
