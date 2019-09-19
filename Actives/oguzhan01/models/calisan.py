# -*- coding: utf-8 -*-

from odoo import models, fields


class Employee(models.Model):
    _name = 'oguzhan.employee'
    _description = 'Çalışan Tanımlama'

    sicil = fields.Char(string='Sicil No', required=True)
    name = fields.Char('İsim', required=True)
    departman_id = fields.Many2one('oguzhan.department', string='Departman', required=True)

class Department(models.Model):
    _name = 'oguzhan.department'
    _description = 'Departman Tanımlama'
    _rec_name = 'departman'

    departman = fields.Selection([('arge', 'AR-GE'),
                                  ('yardimci_sanayi', 'Yardımcı Sanayi'),
                                  ('uretim', 'Üretim'),
                                  ('ik', 'İnsan Kaynakları')],
                                 string='Departman')
    sicil_id = fields.One2many('oguzhan.employee', 'id', string='Sicil', required=True)

# class EmployeeDepartment(models.Model):
#
#     _name = 'oguzhan.employeedepartment'
#     _description = 'Çalışan - Departman Tanımlama'

