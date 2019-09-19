from odoo import models, fields


class Equipment(models.Model):
    _name = "debit.equipment"
    _description = "Malzeme Bilgileri"

    employee_ids = fields.One2many('hr.employee', 'job_id', string='Employees', groups='base.group_user')
    department_id = fields.Many2one('hr.department', string='Department')

    t_no = fields.Char(string="TNO")
    dmb_no = fields.Char(string="DMBNO")
    eq_name = fields.Selection([('1', 'Bilgisayar'),
                                ('2', 'Ekran')],
                               string="Malzeme Adı")
    brand = fields.Char(string="Marka")
    model = fields.Char(string="Model")
    serial_no = fields.Char(string="Seri No")
    location = fields.Selection([("İst","İstanbul Teknopark"),
                                 ("İst 2", "Yıldız Teknik"),
                                 ("Ank", "Akıncı")],
                                string="Yer")
    fr_no = fields.Char(string="FR NO")
    arrive_date = fields.Datetime(string="GELİŞ TR.")

