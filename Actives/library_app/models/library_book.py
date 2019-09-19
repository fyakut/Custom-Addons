from odoo import api, fields, models
from odoo.exceptions import Warning

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'

# For logic operations, we use @api.multi
    @api.multi
    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3]*6
            terms = [a*b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    @api.multi
    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise Warning('Please provide an ISBN for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
        return True

    name = fields.Char('Title', required=True)
    isbn = fields.Char('ISBN')
    active = fields.Boolean('Active?', default=True)
    date_published = fields.Date()
    image = fields.Binary('Cover')
    # Bir kitabın bir yayıncısı olabilir, bir yayıncının birden çok kitabı olabilir.
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    # Bir kitabın birden fazla yazarı olabilir, bir yazar birden fazla kitap yazabilir.
    author_ids = fields.Many2many('res.partner', string='Authors')