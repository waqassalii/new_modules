# -*- coding: utf-8 -*-
# from odoo import http


# class ApiShipengine(http.Controller):
#     @http.route('/api_shipengine/api_shipengine/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/api_shipengine/api_shipengine/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('api_shipengine.listing', {
#             'root': '/api_shipengine/api_shipengine',
#             'objects': http.request.env['api_shipengine.api_shipengine'].search([]),
#         })

#     @http.route('/api_shipengine/api_shipengine/objects/<model("api_shipengine.api_shipengine"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('api_shipengine.object', {
#             'object': obj
#         })
