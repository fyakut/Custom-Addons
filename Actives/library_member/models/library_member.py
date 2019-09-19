from odoo import fields, models


class Member(models.Model):

    _name = 'library.member'
    _description = 'Library Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    card_number = fields.Char()

    partner_id = fields.Many2one(
        'res.partner',

        delegate=True,
        # Parent tablodan silinen veri, child'dan da silinir.
        ondelete='cascade',
        required=True)

    # "res_partner" tablosunda PK olan "id", "library_member" tablosundaki "partner_id" ile ilişkilendirilir(FK olur).
    # Delegational inheritance (delegate=True) => _inherits={'res.partner':'partner_id'} yerine.;
    # "res_partner" tablosundaki her attribute'u bu modelin view'ında kullabilmemizi sağlar.
    # Bu modelin view'ında, "res_partner" modelinin "required=True" kısımları bulunmak zorundadır.
    ## Çünkü "library_member" tablosuna yapılacak kayıt, kendi attribute'larıyla "res_partner"a da yapılacak.
