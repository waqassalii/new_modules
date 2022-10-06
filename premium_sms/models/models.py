# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api


class PremiumSms(models.Model):
    _name = 'premium.sms'
    _description = 'premium_sms.premium_sms'

    phone = fields.Char()
    doc_ref = fields.Char()
    message = fields.Text()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('failed', 'Failed to Delivery'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')


class AccountPaymentInherit(models.Model):
        _inherit = 'account.payment'

        def action_post(self):
            res = super(AccountPaymentInherit, self).action_post()
            message = "DEAR MEMBER %s \n RECORD UPDATE : \n You are Credit of %s on %s" % (self.partner_id.name, self.amount_total, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            vals={
                'phone': self.partner_id.phone,
                'doc_ref': self.name,
                'message': message,
            }
            premium = self.env['premium.sms'].create(vals)
            return res


class PosOrderInherit(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create(self, values):
        res = super(PosOrderInherit, self).create(values)
        message_order = ''
        shop = ''
        for line in res.lines:
            message_order += "Product: %s \n Qty: %s \n Unit Price %s \n Subtotal %s \n" % (line.product_id.name, line.qty,
                                                                                line.price_unit, round(line.price_subtotal, 2))
            shop = line.name
        message = "Hello %s  \n POS %s with Total amount :%s \n and your order details are \n %s" % (res.partner_id.name, res.session_id.name, round(res.amount_total, 2), message_order)
        vals = {
            'phone': res.partner_id.phone,
            'doc_ref': shop,
            'message': message,
        }

        premium = self.env['premium.sms'].create(vals)
        return res
