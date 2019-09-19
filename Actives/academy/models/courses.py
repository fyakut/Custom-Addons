from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class Courses(models.Model):
    _name = "academy.courses"
    _description = "Courses In Our Company"

    name = fields.Char(string="Course Name", requried=True)
    teacher = fields.Many2many("hr.employee", relation="course_teacher",
                               column1="course_ids", column2="hr_teacher_ids")
    priority = fields.Selection([
        ('mandatory', 'Mandatory'),
        ('optional', 'Optional'),
    ], string="Priority")
    employee_ids = fields.Many2many("hr.employee", relation="course_employee",
                                    column1="course_ids", column2="hr_employee_ids")
    course_no = fields.Integer(string="Course Number")
    duration = fields.Integer(string="Duration")
    expiry_date = fields.Date(string="Expiry Date")
    start_date = fields.Date()
    expiry_status = fields.Selection([
        ('valid', 'Valid'),
        ('invalid', 'Invalid'),
    ], readonly=True, compute='_compute_expiry_status', store=True)

    @api.onchange('start_date', 'duration')
    def _compute_expiry_date(self):
        for course in self:
            if course.start_date and (course.duration > 0):
                course.expiry_date = course.start_date + timedelta(days=365 * course.duration)

    @api.depends('expiry_date')
    def _compute_expiry_status(self):
        for course in self:
            if course.expiry_date and course.start_date:
                time_left = (course.expiry_date - fields.Date.today()).days
                if time_left > 0:
                    course.expiry_status = 'valid'
                else:
                    course.expiry_status = 'invalid'


