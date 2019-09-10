from odoo import models, fields

class aeronix(models.Model):
    _name = 'aeronix.aeronix'
    _description = 'Emploeyee certificates'

    name = fields.Many2one('hr.employee')
    type = fields.Selection([('passport','Passport'),
                             ('id_card','ID Card'),
                             ('driving_license','Driving License')], string='Type')
    id_no = fields.Char(string='ID Number')
