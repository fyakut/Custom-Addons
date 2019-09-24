from odoo import api, models, fields
from dateutil.relativedelta import relativedelta as delta
from odoo.exceptions import ValidationError

class Personnel(models.Model):
    _inherit = 'hr.employee'
    _sql_constraints = [
        ('personnel_sicil_uq',  # Constraint unique identifier
         'UNIQUE (sicil_no)',  # Constraint SQL syntax
         'Sicil No must be unique'),  # Message
    ]

    rank = fields.Char(string='Rank')
    sicil_no = fields.Char(string='Sicil No')

    start_date = fields.Date(string='Start Date', default=fields.date.today())
    service_time = fields.Char(string='Time Worked', compute='_compute_service_time', store=True)

    @api.depends("start_date")
    def _compute_service_time(self):
        ## İki tarih arası yıl, ay, gün hesaplayan class
        for record in self:
            if record.ensure_one():
                time_worked = delta(fields.date.today(), record.start_date)
                if (time_worked.days < 0) or (time_worked.months < 0) or (time_worked.years < 0):
                    raise ValidationError('Start date is selected beyond today !!!')
                else:
                    ## Burda da güzel bir hale dönüştürüyoruz.
                    record.service_time = str(time_worked.years) + ' year(s) ' + str(time_worked.months) + ' month(s) ' + str(time_worked.days) + ' day(s)'
