# -*- coding: utf-8 -*-
{
    'name': "sh5000",

    'summary': """
        first module - build step by step""",

    'description': """
        5000 list - build step by step
    """,

    'author': "sh 5000",
    'website': "http://www.sh5000.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/views.xml',
        'reports/report.xml',
        'views/templates.xml',
        'views/demo_sh5000_template.xml'
    ],

    # 'data': [
    #     'security/security.xml',
    #     'security/ir.model.access.csv',
    #     'data/data_demo_odoo.xml',
    #     'views/menu.xml',
    #     'views/view.xml',
    #     'reports/report.xml',
    #     'views/demo_odoo_template.xml',
    # ],
    # only loaded in demonstration mode

    # 'demo': [
    #     'demo/demo.xml',
    # ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
