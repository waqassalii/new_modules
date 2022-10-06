# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    check_in_latitude = fields.Float(
        "Check-in Latitude", digits="Location", readonly=True
    )
    check_in_longitude = fields.Float(
        "Check-in Longitude", digits="Location", readonly=True
    )
    check_out_latitude = fields.Float(
        "Check-out Latitude", digits="Location", readonly=True
    )
    check_out_longitude = fields.Float(
        "Check-out Longitude", digits="Location", readonly=True
    )

    checkin_link = fields.Char(string="Check-In Map Location", compute='_get_checkin_map')
    checkout_link = fields.Char(string="Check-Out Map Location", compute='_get_checkin_map')

    def _get_checkin_map(self):
        for rec in self:
            if rec.check_in_latitude and rec.check_in_longitude:
                rec.checkin_link = "https://maps.google.com/?q=" + str(rec.check_in_latitude) + "," + str(rec.check_in_longitude)
            else:
                rec.checkin_link = False
            if rec.check_out_latitude and rec.check_out_longitude:
                rec.checkout_link = "https://maps.google.com/?q=" + str(rec.check_out_latitude) + "," + str(rec.check_out_longitude)
            else:
                rec.checkout_link = False