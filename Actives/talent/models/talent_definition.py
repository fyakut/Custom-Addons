from odoo import models, fields, api

class Talent(models.Model):
    _name = 'talent.definition'
    _description = 'Skills'
    _sql_constraints = [
        (
            'talent_uq',
            'unique(name, talent_level)',
            'Existing Record !!'
        ),
    ]
    name = fields.Char('Talent Name', required=True)
    talent_level = fields.Selection([('1', 'Beginner'),
                                     ('2', 'Intermediate'),
                                     ('3', 'Advanced')], required=True)
    employee_ids = fields.Many2many('talent.employee', string='Talent')
