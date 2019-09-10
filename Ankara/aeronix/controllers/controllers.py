# -*- coding: utf-8 -*-
from odoo import http

# class Aeronix(http.Controller):
#     @http.route('/aeronix/aeronix/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aeronix/aeronix/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aeronix.listing', {
#             'root': '/aeronix/aeronix',
#             'objects': http.request.env['aeronix.aeronix'].search([]),
#         })

#     @http.route('/aeronix/aeronix/objects/<model("aeronix.aeronix"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aeronix.object', {
#             'object': obj
#         })