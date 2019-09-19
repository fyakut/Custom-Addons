from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    course_ids = fields.Many2many("academy.courses", relation="course_employee",
                                    column1="hr_employee_ids", column2="course_ids")
