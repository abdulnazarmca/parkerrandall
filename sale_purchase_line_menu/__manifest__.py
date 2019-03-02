# -*- coding: utf-8 -*-
{
    'name': "Sale Purchase Line Menu",

    'summary': """
        Temp menu for sale and Purchase order line""",

    'author': "Abdul Nazar",
    'website': "http://www.pr-uae.com",

    'category': 'Parker Randall',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
	'views/model_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
