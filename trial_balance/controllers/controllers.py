# -*- coding: utf-8 -*-
# from odoo import http


# class TrialBalance(http.Controller):
#     @http.route('/trial_balance/trial_balance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trial_balance/trial_balance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('trial_balance.listing', {
#             'root': '/trial_balance/trial_balance',
#             'objects': http.request.env['trial_balance.trial_balance'].search([]),
#         })

#     @http.route('/trial_balance/trial_balance/objects/<model("trial_balance.trial_balance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trial_balance.object', {
#             'object': obj
#         })
