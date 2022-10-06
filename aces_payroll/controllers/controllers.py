# -*- coding: utf-8 -*-
# from odoo import http


# class AcesPayroll(http.Controller):
#     @http.route('/aces_payroll/aces_payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aces_payroll/aces_payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aces_payroll.listing', {
#             'root': '/aces_payroll/aces_payroll',
#             'objects': http.request.env['aces_payroll.aces_payroll'].search([]),
#         })

#     @http.route('/aces_payroll/aces_payroll/objects/<model("aces_payroll.aces_payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aces_payroll.object', {
#             'object': obj
#         })
