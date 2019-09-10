{
 'name': 'Personel Data',
 'description': 'Personel Data',
 'summary': 'Knowledge about the personel in TUSAS',
 'author': ':)',

 'depends': [
     'base',
     'hr',
 ],
 'data': [
    # 'security/ir.model.access.csv',
    'views/hr_employee.xml',
 ],

 'application': True,
 'installable': True,
}