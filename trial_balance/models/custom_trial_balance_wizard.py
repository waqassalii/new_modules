# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomTrialBalanceWizard(models.TransientModel):
    """ Wizard allowing to grant a badge to a user"""
    _name = 'custom.trial.balance.wizard'
    _description = 'Custom trial balance'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    data_type = fields.Selection([
        ("all", "All"),
        ("posted", "Posted"),
        ("unposted", "Unposted"),
    ], string="Select Type", default='all')

    def action_print_pdf(self):
        return self.env.ref('trial_balance.action_trial_balance_report_id').report_action(self, data=None)

    def action_get_move_line(self):
        print('move line function is called.....')
        move_lines = self.env['account.move.line'].search([('date_maturity', '>', self.date_from),
                                                           ('date_maturity', '<', self.date_to)])
        print('move_lines is calling.....', move_lines)
        return move_lines
        # for line in move_lines:
        #     print('line is printing here', line)
        #     # return True


