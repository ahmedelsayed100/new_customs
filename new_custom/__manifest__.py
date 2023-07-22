# -*- coding: utf-8 -*-
{
    'name': "Employee Payment",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ahmed Hussein",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # 'data/sequence.xml',
        'security/security.xml',
        'reports/report.xml',
        'views/group.xml',
        'views/views.xml',
        'wizard/hr_travel_reason_wizard.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}