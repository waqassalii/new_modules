import os

from odoo import models, fields, api
from ..tools.shipengine import ShipEngine
from ..tools.shipengine.errors import ShipEngineError

class Shipengine(models.Model):
    _name = 'ship.engine'
    _description = 'Ship Engine'

    name = fields.Char('Ship Engine')
    reference = fields.Char()
    ship_engine_id = fields.Char()
    ship_engine_object = fields.Text('Object')

    def authenticate(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('shipengine_api.key')
        shipengine = ShipEngine(
            {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
        )
        return shipengine

class ShipEngineServices(models.Model):
    _name = 'ship.engine.service'

    engine_carrier_id = fields.Char('Carrier ID')
    engine_carrier_code = fields.Char('Carrier Code')
    engine_service_code = fields.Char('Service Code')
    engine_name = fields.Char('Name')
    engine_domestic = fields.Boolean('Domestic')
    engine_international = fields.Boolean('International')
    engine_is_multi_package_supported = fields.Boolean('Multi Package Supported')
    delivery_id = fields.Many2one('delivery.carrier')