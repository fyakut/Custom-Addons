{
 'name': 'Personel Zimmet Listesi',
 'description': 'Personellere ait malzeme listesi',
 'author': 'Koray Uymaz',

 'depends': [
     'base',
     'hr',
 ],
 'data': [
    'security/ir.model.access.csv',
    'views/debit.xml',
 ],

 'application': True,
 'installable': True,
}