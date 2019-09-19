{'name': 'PDKS Module',
 'description': 'Testing What I have learned',
 'author': 'Koray Uymaz',
 'depends': ['base',
             'hr_attendance'],
 'data': [
    'security/pdks_security.xml',
    'security/ir.model.access.csv',
    'views/pdks_menu.xml',
    'views/pdks_view.xml',

 ],
 'application': True,
 'installable': True,
 }