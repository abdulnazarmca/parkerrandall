# -*- coding: utf-8 -*-
{
    'name': 'Account Partner Statement',
    'version': '1.0',
    'category': 'Account',
    'description': "",
    'author': "Abdul Nazar, Parker Randall",
    'depends': ['base', 'account'],
    'data': [
        'wizard/statement_view.xml',
        'report/report.xml',
        'report/report_partner_statement.xml',
        'security/ir.model.access.csv',
            ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
