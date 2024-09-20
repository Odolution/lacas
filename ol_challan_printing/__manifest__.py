{
    'name': "Challan Printing",
    'description': "",
    'category': 'customization',
    'sequence': -10,
    'version': '1.0',
    'depends': [ 'mail', 'base' ], 
    'data': [
        'security/ir.model.access.csv',
        'views/menu_items.xml',
        'views/challan_printing.xml',
    ],
    'demo' : [] ,
    'qweb' : [],
    'installable' : True, 
    'application' : True,
    'auto_install' : False,
    'license': 'LGPL-3',
}