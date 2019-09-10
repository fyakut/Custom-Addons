from odoo.odoo import models, fields, api
from odoo.odoo.exceptions import Warning


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


class Employee(models.Model):
    _name = 'talent.employee'
    _description = 'Employees'

    name = fields.Many2one('hr.employee', string='Employee Name')
    email = fields.Char(string='E-Mail')
    department_id = fields.Char(string='Department')
    role_id = fields.Char(string='Role')

    talent_id = fields.Many2many('talent.definition', string='Talent')

    @api.onchange('name')
    def _onchange_name(self):
        self.email = self.name.work_email
        self.role_id = self.name.job_id.name
        self.department_id = self.name.department_id.name

    @api.constrains('talent_id')
    def _check_same_talent(self):
        records = []
        for record in self.talent_id:
            records.append(record.name.lower())
        for i in range(len(records)):
            for j in range(len(records)):
                if i == j:
                    pass
                elif records[i] == records[j]:
                    raise Warning('Same Talent Selected !!!')
