# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.tools.safe_eval import pytz


class CustomTrialBalance(models.Model):
    """ Wizard allowing to grant a badge to a user"""
    _name = 'custom.trial.balance'
    _description = 'Custom trial balance'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def action_move_line(self):
        print('action is calling.....')
        move= self.env['account.move'].search([])
        move_lines= self.env['account.move.line'].search([('date_maturity', '>', self.date_from),
                                                          ('date_maturity', '<', self.date_to)])
        print('move is calling.....', move)
        print('move_lines is calling.....', move_lines)



