from odoo import api, models, fields
from dateutil.relativedelta import relativedelta as delta


class Personnel(models.Model):
    _inherit = 'hr.employee'
    _sql_constraints = [
        ('personnel_sicil_uq',  # Constraint unique identifier
         'UNIQUE (sicil_no)',  # Constraint SQL syntax
         'Sicil No must be unique'),  # Message
    ]

    rank = fields.Char(string='Rank')
    sicil_no = fields.Char(string='Sicil No')

    start_date = fields.Date(string='Start Date')
    service_time = fields.Char(string='Time Worked')

    @api.onchange('start_date')
    def _compute_service_time(self):
        ## İki tarih arası yıl, ay, gün hesaplayan class
        time_worked = delta(fields.datetime.now(), self.start_date)
        ## Burda da güzel bir hale dönüştürüyoruz.
        self.service_time = str(time_worked.years) + ' year(s) ' + str(time_worked.months) + ' month(s) '+ str(time_worked.days) + ' day(s)'
