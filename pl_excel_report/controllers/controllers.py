# -*- coding: utf-8 -*-
# from odoo import http


# class PlExcelReport(http.Controller):
#     @http.route('/pl_excel_report/pl_excel_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pl_excel_report/pl_excel_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pl_excel_report.listing', {
#             'root': '/pl_excel_report/pl_excel_report',
#             'objects': http.request.env['pl_excel_report.pl_excel_report'].search([]),
#         })

#     @http.route('/pl_excel_report/pl_excel_report/objects/<model("pl_excel_report.pl_excel_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pl_excel_report.object', {
#             'object': obj
#         })
