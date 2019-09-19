from random import choice
from string import digits

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PdksYetki(models.Model):
    _name = "pdks.authority"
    _description = "Yetki Tanımlama"

    def _default_random_badge(self):
        badge = None
        while not badge or self.env['pdks.authority'].search([('badge', '=', badge)]):
            badge = "".join(choice(digits) for i in range(6))
        return badge

    badge = fields.Char(string='Sicil', default=_default_random_badge, required=True)
    department_code = fields.Char(string='Bölüm Kodu')
    card_no = fields.Integer(string='Kart No')
    image = fields.Binary('Cover')

    area_id = fields.Many2many('pdks.areas', 'pdks_id', string='Alan Yetkileri')
    name = fields.Many2one(
        'hr.employee',
        delegate=True,
        ondelete='cascade',
        required=True)