{
    'name': 'custom withdrawals',
    'version': '1.1',
    'summary': 'Custom',
    'sequence': 10,
    'description': """Customization in odoo modules  """,
    'category': 'Services',
    'license': 'LGPL-3',
    'images': [],
    'depends': ['account', 'account_accountant',"old_depreciated_fields"],
    'data': [

        'views/academics_tab.xml',


    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
