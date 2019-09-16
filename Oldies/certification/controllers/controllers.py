# -*- coding: utf-8 -*-
from odoo import http

# class Certification(http.Controller):
#     @http.route('/certification/certification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/certification/certification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('certification.listing', {
#             'root': '/certification/certification',
#             'objects': http.request.env['certification.certification'].search([]),
#         })

#     @http.route('/certification/certification/objects/<model("certification.certification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('certification.object', {
#             'object': obj
#         })