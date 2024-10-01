{
    'name': 'Invoice Fields',

    "author": "Muhammad Omer Siddiqui",
    'version': '0.1',
    'category': 'Invoice Customization',
    'sequence': 97,
    'description': "Add new fields in account.move",
    'website': '',
    'depends': ["base","account","ol_lacas_custom_trees"],
    'data': [
        
        "views/account_view.xml",

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