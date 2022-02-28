# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'OnlineShop Ex1',
    'version': '1.3',
    'sequence': 10,
    'description': """ """,
    'category': 'Productivity',
    'license': 'LGPL-3',
    'depends': ['sale', 'contacts'],
    'data': [
        'views/customer.xml',
        'views/product.xml',
        'views/customer_valid.xml',
        'views/show_code_on_my_cart_template.xml',
        'security/security.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [],
    'qweb': [],
    'installable': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
