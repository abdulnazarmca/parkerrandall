# -*- coding: utf-8 -*-
{
    'name': "Ethoscorp Trading upgrades",

    'summary': """
        Simple module to add various improvements to carry extra info for trading""",

    'description': """
        current features
        - adding short description
        planned features
        - adding automatic copy of short description from the source SO/POs (TBD) when copied
    """,

    'author': "Abdul Nazar",
    'website': "http://www.pr-uae.com",

    'category': 'Parker Randall',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','purchase','account','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
	'views/purchase_order_view.xml',
	'views/sale_order_view.xml',
	'views/account_invoice_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
