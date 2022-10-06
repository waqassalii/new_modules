# -*- coding: utf-8 -*-
# from odoo import http


# class PremiumSms(http.Controller):
#     @http.route('/premium_sms/premium_sms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/premium_sms/premium_sms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('premium_sms.listing', {
#             'root': '/premium_sms/premium_sms',
#             'objects': http.request.env['premium_sms.premium_sms'].search([]),
#         })

#     @http.route('/premium_sms/premium_sms/objects/<model("premium_sms.premium_sms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('premium_sms.object', {
#             'object': obj
#         })
