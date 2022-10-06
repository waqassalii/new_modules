from odoo import models,fields,_

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_ship_engine_rates(self):
        return {
            'name': _('ShipEngine Rates'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'shipengine.rate',
            'target': 'new',
        }