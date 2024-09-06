# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Real time Stock Inventory Valuation Report (PDF/EXCEL) in odoo',
    'version': '16.0.0.1',
    'category': 'Warehouse',
    'price': 69,
    'currency': "EUR",
    'summary': 'print product inventory Valuation Report real time stock inventory report for particular date Stock Inventory Real Time Report stock card stockcard inventory cost reports real time inventory valuation report Periodically Stock valuation Report stock report',
    'description': """
   
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    'depends': ['sale','account'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/assets.xml',
        # 'report/report_pdf.xml',
        'report/inventory_valuation_detail_template.xml',
        'wizard/sales_daybook_report_product_category_wizard.xml',
    ],
    'live_test_url':'https://youtu.be/Lpr2cqdzs_I',
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images":["static/description/Banner.png"],
    'assets': {
        
        'web.assets_backend': [
            
            'bi_inventory_valuation_reports/static/src/js/select_all_records.js',
        ],
    },
    "license":'OPL-1',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

