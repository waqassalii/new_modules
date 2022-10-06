# -*- coding: utf-8 -*-
{
    'name': 'Import Sale Order Data',
    'version': '14.0.0.3',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': 'https://www.pragtech.co.in',
    'summary': 'Easy to import odoo data of sale orders through Excel import/CSV import import sale order odoo import sale order import sale order data sale order data sale order import',
    'description': """
Import sale order from Excel and CSV file.
<keywords>
import sale order
odoo import sale order
import sale order data
sale order data
sale order import
    """,
    'depends': ['base', 'sale_management', 'stock', 'account', ],
    'data': [
        'security/ir.model.access.csv',
        'security/import_security_sale_order.xml',
        'views/sale_order_view.xml',
        'views/sale_order_line_view.xml',
    ],
    'images': ['static/description/Animated-import-sale-order.gif'],
    'live_test_url': 'https://www.pragtech.co.in/company/proposal-form.html?id=103&name=import-sales-order-data',
    'license': 'OPL-1',
    'price': 10,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
}
