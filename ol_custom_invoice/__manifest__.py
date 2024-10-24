
{
    'name': 'Custom Invoice',

    "author": "Muhammad Omer Siddiqui",
    'version': '0.1',
    'category': 'Invoice Customization',
    'sequence': 95,
    'summary': 'Implementation of Custom charges of specific product  in Invoice.',
    'description': "Implementation of Custom charges of specific product  in Invoice.",

    'depends': ["base","account","ol_lacas_custom_trees"],
    'data': [
        'view/custom_invoice_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

    'license': 'LGPL-3',
}