from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PdksAreas(models.Model):
    _name = "pdks.areas"
    _description = "Alan Tanımlama"

    pdks_id = fields.Many2many('pdks.authority', string='Pdks')
    area_id = fields.Text(string='Field Code', required=True)
    area_name = fields.Char(string='Field Name', required=True)
    area_type = fields.Selection([('S', 'Hassas Bölgeler'),
                                  ('O', 'Kontrollü Bölge'),
                                  ('Y', 'Yetki Girişli Bölge'),
                                  ('G', 'Şirket Giriş Noktası')],
                                 string='Alan Tipi')
    building_id = fields.Selection([('170', '170 Nolu Bina'),
                                    ('171', '171 Nolu Bina')],
                                   string='Bina Kodu')
    area_points = fields.Selection([('170', '170 - A1 Bilgi Yönetimi Sistemleri'),
                                    ('170-a', '170 - A2 Uçuşa el verişlilik ve emniyet'),
                                    ('170-b', 'AZ Tedarik')],
                                   string='Nokta ve Bölgeler')


    @api.onchange('area_id')
    def _onchange_area_id(self):
        if self.area_id:
            res = self.area_id
            if len(res) >= 6:
                raise ValidationError('Not a valid Field Code')
            
class PdksTerminal(models.Model):
    _name = "pdks.terminal"
    _description = "Terminal Tanımlama"

    pdks_id = fields.Many2one('pdks.authority', string='Pdks')
    device_id = fields.Text(string='Cihaz ID')
    ip_no = fields.Text(string='IP No')
    terminal_no = fields.Text(string='Terminal No')
    terminal_type = fields.Selection([('office', 'Ofis'),
                                      ('enterance', 'Giriş Kapıları')],
                                     string='Terminal Tipi')
    enter_code = fields.Selection([('enter_code_1', 'Giriş Kodu 1'),
                                   ('enter_code_2', 'Giriş_Kodu_2')],
                                  string='Giriş Kodu')
    exit_code = fields.Selection([('exit_code_1', 'Çıkış Kodu 1'),
                                   ('exit_code_2', 'Çıkış_Kodu_2')],
                                  string='Çıkış Kodu')
    area = fields.Selection([('area_1', 'Alan 1'),
                                  ('area_2', 'Alan_2')],
                                 string='Alan')
    explanation = fields.Text(string='Açıklama')
    column = fields.Text(string='Kolon')







