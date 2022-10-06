# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OmMenu(http.Controller):
    @http.route('/om-menu/<string:name>', auth='public')
    def index(self, **kw):
        if kw.get('name') and not kw.get('id'):
            restaurant = request.env['vendor.restaurant'].sudo().search([('short_name','=',kw.get('name'))])
            if restaurant:
                pro = []
                categories = restaurant.category_line_ids
                for category in categories:
                    for product in category.restaurant_product_line:
                        pro.append(product.id)
                products = request.env['vendor.restaurant.product'].sudo().browse(pro)
                value = {"restaurant":restaurant,
                          "categories":categories,
                           "products":products}
                return request.render("om_menu.om_menu_template", value)
            else:
                return 'Restaurant does not exit.'
        if kw.get('name') and kw.get('id'):
            restaurant = request.env['vendor.restaurant'].sudo().search([('short_name', '=', kw.get('name'))])
            categories = []
            if restaurant:
                pro = []
                products = request.env['vendor.restaurant.product'].sudo().search([('category_id','=',int(kw.get('id')))])

                value = {
                    "restaurant": restaurant,
                    "categories": categories,
                    "products": products}

                return request.render("om_menu.om_menu_product_template", value)
            else:
                return 'Restaurant does not exit.'
        else:
            return 'Restaurant does not exit.'


class OmMenuContact(http.Controller):
    @http.route('/om-menu/contactus/<string:name>', auth='public')
    def index(self, **kw):
        if kw.get('name'):
            restaurant = request.env['vendor.restaurant'].sudo().search([('short_name', '=', kw.get('name'))])
            if restaurant:
                value = {
                    "restaurant": restaurant}

                return request.render("om_menu.om_menu_contact_template", value)
            else:
                return 'Restaurant does not exit.'

        else:
            return 'Restaurant does not exit.'

