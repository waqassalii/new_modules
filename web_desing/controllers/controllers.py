# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebDesing(http.Controller):
    @http.route('/web-design/odd-menu', auth='public')
    def generate_web_design(self, **kw):
        # return 'hellow world'
        return request.render('web_desing.web_design_odd_menu', {})
    #
    # @http.route('/web_desing/web_desing/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('web_desing.listing', {
    #         'root': '/web_desing/web_desing',
    #         'objects': http.request.env['web_desing.web_desing'].search([]),
    #     })
    #
    # @http.route('/web_desing/web_desing/objects/<model("web_desing.web_desing"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('web_desing.object', {
    #         'object': obj
    #     })
