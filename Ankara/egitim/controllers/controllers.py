# -*- coding: utf-8 -*-
from odoo import http

# class Egitim(http.Controller):
#     @http.route('/egitim/egitim/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/egitim/egitim/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('egitim.listing', {
#             'root': '/egitim/egitim',
#             'objects': http.request.env['egitim.egitim'].search([]),
#         })

#     @http.route('/egitim/egitim/objects/<model("egitim.egitim"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('egitim.object', {
#             'object': obj
#         })