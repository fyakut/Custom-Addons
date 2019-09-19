{

    'name': 'Certification',
    'summary': "Defines certification for different purposes.",
    'author': "Eficent, Odoo Community Association (OCA)",
    'website': "https://github.com/oguzhandikici",
    'category': 'Certification Management',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': ['security/certification_security.xml',
             'security/ir.model.access.csv',
             'views/certification_view.xml',
             'views/certification_standart_view.xml',
             'views/res_partner_view.xml',
             'views/certification_bodies_view.xml',
             'reports/certification_report_view.xml',
             'reports/certification_report_pdf.xml',
             'reports/certification_template_pdf.xml',
             ],
    'demo': ['data/certification_demo.xml'],
    'development_status': 'Beta',
    'maintainers': ['ceeficent']
}
