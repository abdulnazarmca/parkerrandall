# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Query Interface',
    'version': '0.1',
    'author': 'Abdul Nazar Pioneer Solution',
    'category': 'Extra',
    'complexity': 'easy',
    'description': """
Query Interface
====================================

This module is used to generate the Query view the result inside the openerp text box.
    """,

    'depends': ['base',],
    'data': [
        'wizard/query_view.xml',
    ],
    'auto_install': False,

}
