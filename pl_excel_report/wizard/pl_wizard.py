# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomPandL(models.TransientModel):
    """ Wizard allowing to grant a badge to a user"""
    _name = 'custom.pl.wizard'
    _description = 'CustomPandL'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def print_custom_pl_excel_report(self):
        print('excel report being printed now')
        # analytical_accounts = self.env['account.analytic.account'].search([])
        # # print('analytical account', analytical_accounts)
        data = {}
        return self.env.ref('pl_excel_report.custom_pl_excel_report_id').report_action(self, data=data)
