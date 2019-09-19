{
'name': 'Yetki Ekranı',
'description': 'Çalışan bina yetkilendirilmesi.',
'author': 'Koray Uymaz',
'data': [
    'security/ir.model.access.csv',
    'views/pdks.xml'
],
'depends': [
    'base',
    'my_addon',
    'hr'
],
'application': False,
}