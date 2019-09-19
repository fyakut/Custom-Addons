from odoo import fields, models

class Employee(models.Model):
    _inherit = "hr.employee"
    _description = "Tusas için olmayan özelliklerin eklenmesi"

    sicil = fields.Char("Sicil No")

class Department(models.Model):
    _inherit = "hr.department"

    department_code = fields.Char(string="Bölüm Kodu")



def hi():
    a= 1
    for c in range(1399):
        print("vay be" +  "**"*a)
        a += 1