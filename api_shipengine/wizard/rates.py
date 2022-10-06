from odoo import fields, models,api,_
from ..tools.shipengine.errors import ShipEngineError
import datetime

class ShipEngineRates(models.TransientModel):
    _name = "shipengine.rate"

    line_ids = fields.One2many('shipengine.rate.line','ship_engine_id')

    def get_shipping_record(self):
        print('im calling inside the wizard')
        orders = self.env['sale.order'].browse(self._context.get('active_ids'))
        my_list = []
        for line in self.line_ids:
            if line.select == True:
                print('im in true selection')
                product = self.env['product.product'].search([('name', '=', line.carrier_nickname)])
                print('products...........', product)
                if product:
                    print('products are available.....')
                    my_list.append((0,0,{
                        'product_id': product.id,
                        'product_uom_qty': 1,
                        'price_unit': line.shipping_amount,
                    }))
                else:
                    self.env['product.template'].create({
                        'name': line.carrier_nickname
                    })
        return orders.write({'order_line': my_list,})

    @api.model
    def default_get(self, default_fields):
        res = super(ShipEngineRates, self).default_get(default_fields)
        try:
            shipengine = self.env['ship.engine'].authenticate()
            shipment = {
                "rate_options": {"carrier_ids": ["se-2823506","se-2823507","se-2823508"]},
                "shipment": {
                    "validate_address": "no_validation",
                    "ship_to": {
                        "name": "Amanda Miller",
                        "phone": "555-555-5555",
                        "address_line1": "525 S Winchester Blvd",
                        "city_locality": "San Jose",
                        "state_province": "CA",
                        "postal_code": "95128",
                        "country_code": "US",
                        "address_residential_indicator": "yes",
                    },
                    "ship_from": {
                        "company_name": "Example Corp.",
                        "name": "John Doe",
                        "phone": "111-111-1111",
                        "address_line1": "4008 Marathon Blvd",
                        "address_line2": "Suite 300",
                        "city_locality": "Austin",
                        "state_province": "TX",
                        "postal_code": "78756",
                        "country_code": "US",
                        "address_residential_indicator": "no",
                    },
                    "packages": [{"weight": {"value": 5, "unit": "ounce"}}],
                },
            }
            '%Y-%m-%d %H:%M:%S'
            result = shipengine.get_rates_from_shipment(shipment=shipment)
            update = []
            for record in result['rate_response']['rates']:
                update.append((0, 0, {
                    'carrier_nickname': record['carrier_nickname'],
                    'service_type': record['service_type'],
                    'service_code': record['service_code'],
                    'ship_date': datetime.datetime.strptime(record['ship_date'].split('T')[0],'%Y-%m-%d'),
                    'shipping_amount': record['shipping_amount']['amount'],
                    'insurance_amount': record['insurance_amount']['amount'],
                    'delivery_days': record['delivery_days'],

                }))
            res.update({'line_ids': update})
            return res
        except ShipEngineError as err:
            print("::ERROR::")
            print(err.to_json())


class ShipEngineRateLines(models.TransientModel):
    _name = "shipengine.rate.line"

    select = fields.Boolean()
    carrier_nickname = fields.Char('Carrier Name')
    service_type = fields.Char()
    service_code = fields.Char()
    ship_date = fields.Date()
    shipping_amount = fields.Float()
    insurance_amount = fields.Float()
    delivery_days = fields.Integer()
    ship_engine_id = fields.Many2one('shipengine.rate')