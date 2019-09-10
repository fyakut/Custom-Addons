# -*- coding: utf-8 -*-
{
    'name': "Tracking Application",

    'summary': """
        This module tracks the movements of device objects assigned to company resources such as employees""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mert İleri, Koray Uymaz, Emine Rumeysa Yılmaz, İdil Kubat, Abdülkadir Yılmaz, Oğuzhan Dikici, Mücahit Taha Az",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Attendance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'application': True,
}
