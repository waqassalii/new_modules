# -*- coding: utf-8 -*-
###################################################################################
#
#    Dynasol Technologies.
#
# sale routes add in sale orders
#
###################################################################################

from odoo import models,fields,api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    route_id = fields.Many2one('sale.route',string='Route')


class SaleRoute(models.Model):
    _name = 'sale.route'
    name= fields.Char(String="Name")

#
# class damages(models.Model):
#     _inherit = 'stock.picking'
#     route_id = fields.Many2one('sale.route', string='Route')
