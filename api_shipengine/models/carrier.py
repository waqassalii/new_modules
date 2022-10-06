from odoo import api, fields, models, _
from ..tools.shipengine.errors import ShipEngineError
class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    engine_carrier_id = fields.Char('Carrier ID')
    engine_carrier_code = fields.Char('Carrier Code')
    engine_account_number = fields.Char('Account Number')
    engine_requires_funded_amount = fields.Char('Requires Funded Amount')
    engine_balance = fields.Float('Balance')
    engine_nickname = fields.Char('Nickname')
    engine_friendly_name = fields.Char('Friendly Name')
    engine_primary = fields.Boolean('Primary')
    engine_has_multi_package_supporting_services = fields.Boolean('Multi Package Supporting Services')
    engine_supports_label_messages = fields.Boolean('Support Label Messages')
    shipengine_services_ids = fields.One2many('ship.engine.service','delivery_id')
    def update_shipping_methods(self):
        try:
            shipengine = self.env['ship.engine'].authenticate()
            result = shipengine.list_carriers()
            for r in result['carriers']:
                is_already = self.env['delivery.carrier'].search([('engine_carrier_id','=',r['carrier_id'])])
                if is_already:
                    pass
                else:
                    product = self.env['product.product'].search([('name','=','FedEx (ShipEngine)')])
                    if product:
                        delivery_product = product[0]
                    else:
                        delivery_product = self.env['product.template'].create({
                            'name' : 'FedEx (ShipEngine)'
                        })
                    vals = {
                        'product_id' : delivery_product.id,
                        'delivery_type': 'fedex',
                        'name' : r['nickname'],
                        'engine_carrier_id' : r['carrier_id'],
                        'engine_carrier_code' : r['carrier_code'],
                        'engine_account_number' : r['account_number'],
                        'engine_requires_funded_amount' : r['requires_funded_amount'],
                        'engine_balance' : r['balance'],
                        'engine_nickname' : r['nickname'],
                        'engine_friendly_name' : r['friendly_name'],
                        'engine_primary' : r['primary'],
                        'engine_has_multi_package_supporting_services' : r['has_multi_package_supporting_services'],
                        'engine_supports_label_messages' : r['supports_label_messages'],
                    }
                    services_list = []
                    for service in r['services']:
                        services_list.append((0,0,{
                            'engine_carrier_id': service['carrier_id'],
                            'engine_carrier_code': service['carrier_code'],
                            'engine_service_code': service['service_code'],
                            'engine_name': service['name'],
                            'engine_domestic': service['domestic'],
                            'engine_international': service['international'],
                            'engine_is_multi_package_supported' : service['is_multi_package_supported']
                        }))
                    vals.update({'shipengine_services_ids':services_list})
                    self.env['delivery.carrier'].create(vals)
            print("::SUCCESS::")
            print(result)
        except ShipEngineError as err:
            print("::ERROR::")
            print(err.to_json())

