from odoo import fields, models

class HrAttandance(models.Model):
    _inherit = 'hr.attendance'
    # employee_id = fields.Many2one('hr.employee', string="Employee", default=_default_employee, required=True,
    #                               ondelete='cascade', index=True)
    # department_id = fields.Many2one('hr.department', string="Department", related="employee_id.department_id",
    #                                 readonly=True)
    # check_in = fields.Datetime(string="Check In", default=fields.Datetime.now, required=True)
    # check_out = fields.Datetime(string="Check Out")
    # worked_hours = fields.Float(string='Worked Hours', compute='_compute_worked_hours', store=True, readonly=True)

