# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomPlXlsx(models.AbstractModel):
    _name = 'report.pl_excel_report.custom_pl_excel_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partner):
        analytical_accounts = self.env['account.analytic.account'].search([])
        branches = self.env['purchase.order'].search([])
        sheet = workbook.add_worksheet('Profit and Loss')
        formate_sub_head = workbook.add_format({'align': 'center', 'font_size': '10', 'text_wrap': True, "border": 1})
        bold = workbook.add_format({'bold': True, 'align': 'center', 'font_size': '10', "border": 1})
        formate_row = workbook.add_format({'bold': True, 'align': 'left'})
        align_left = workbook.add_format({'align': 'left'})
        align_right = workbook.add_format({'align': 'right'})
        align_right_bold = workbook.add_format({'align': 'right', 'bold': True})
        bold_last_header = workbook.add_format({
            'bold': True,
            'align': 'center',
            'text_wrap': True,
            'font_size': '10px',
            "border": 2})

        # header part  header part  header part  header part  header part
        sheet.write(1, 1, '2022', bold)
        sheet.merge_range('C2:J2', 'Branch', bold)
        sheet.write(1, 2, 'Branch', bold)

        for j, branch in enumerate(branches):
            sheet.write(2, 2 + j, branch.partner_id.name, formate_sub_head)

        # cost center cost center cost center cost center cost center cost center
        sheet.merge_range(1, 10, 1, 27, 'Cost Center', bold)
        sheet.write(1, 10, 'Cost Center', bold)
        for j, branch in enumerate(branches):
            sheet.write(2, 10 + j, branch.partner_id.name, formate_sub_head)

        # Analytic Tag Analytic Tag Analytic Tag Analytic Tag Analytic Tag Analytic Tag Analytic Tag
        sheet.merge_range(1, 28, 1, 44, 'Analytic Tag', bold)
        sheet.write(1, 28, 'Analytic Tag', bold)
        for k, account in enumerate(analytical_accounts):
            sheet.write(2, 28 + k, account.name, formate_sub_head)

        # last four head field last four head field last four head field last four head field
        sheet.merge_range(1, 45, 2, 45, 'Nil', bold_last_header)
        sheet.write(2, 45, 'Nil', bold_last_header)
        sheet.merge_range(1, 46, 2, 46, 'Total Branch', bold_last_header)
        sheet.write(2, 46, 'Total Branch', bold_last_header)
        sheet.merge_range(1, 47, 2, 47, 'Total Cost Center', bold_last_header)
        sheet.write(2, 47, 'Total Cost Center', bold_last_header)
        sheet.merge_range(1, 48, 2, 48, 'Total Analytic Tag', bold_last_header)
        sheet.write(2, 48, 'Total Analytic Tag', bold_last_header)
        sheet.merge_range(1, 49, 2, 49, 'Total', bold_last_header)
        sheet.write(2, 49, 'Total', bold_last_header)
        # rows data rows data rows data rows data rows data rows data rows data rows data rows data
        sheet.write(4, 0, 'Income', formate_row)
        sheet.write('A6', 'Gross Profit', formate_row)
        sheet.write('A7', 'Operating Income', align_left)
        sheet.write('A8', 'Cost of Revenue', align_left)
        sheet.write('A9', 'Total Gross Profit', formate_row)
        sheet.write('A10', 'Other Income', formate_row)
        sheet.write('A11', 'Total Income', formate_row)
        sheet.write('A13', 'Expenses', formate_row)
        sheet.write('A14', '5104001-5104999 Bank Charges', align_left)
        sheet.write('A15', '5104001 Bank Charges', align_left)
        sheet.write('A16', '5107001-5107999 Entertainment', align_left)
        sheet.write('A17', '5107001 Meals and entertainment', align_left)
        sheet.write('A45', 'Depreciation', formate_row)
        sheet.write('A46', 'Total Expenses', formate_row)
        sheet.write('A48', 'Net Profit', formate_row)

        sheet.write('B14', '943,370.86Rs.', align_left)
        sheet.write('B15', '943370.86', align_right)
        sheet.write('B16', '49,942.00Rs.', align_left)
        sheet.write('B17', '49942', align_right)
        sheet.write('B46', '8315885.77', align_right_bold)
        sheet.write('B48', '-8315885.77', align_right_bold)
