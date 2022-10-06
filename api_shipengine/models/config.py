# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    shipengine_api_enabled = fields.Boolean("ShipEngine API",
                                             config_parameter='shipengine_api.enabled',
                                             groups='base.group_system')

    shipengine_api_key = fields.Char("API Key",
                                      config_parameter='shipengine_api.key',
                                      groups='base.group_system')


