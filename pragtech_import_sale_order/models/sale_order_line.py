# -*- coding: utf-8 -*-
import binascii
import logging
import tempfile

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import UserError
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)
import io

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class SaleOrderLineWizard(models.TransientModel):
    _name = 'sale.order.line.wizard'
    _description = 'Updated Sale Order Line'

    order_line_file = fields.Binary(string="Upload File")
    import_file_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='File Type', default='csv')
    import_product_option = fields.Selection([('barcode', 'Barcode'), ('code', 'Code'), ('name', 'Name')],
                                             string='Import Product By ', default='name')
    product_select_option = fields.Selection([('from_product', 'Take Details From The Product'), ('from_xls', 'Take Details From The XLS File')],
                                             string='Product Detail Options', default='from_xls')

    def import_sale_order_line(self):
        if self.import_file_option == 'csv':
            keys = ['product', 'quantity', 'uom', 'description', 'price', 'tax']
            try:
                csv_data = base64.b64decode(self.order_line_file)
                data_file = io.StringIO(csv_data.decode("utf-8"))
                data_file.seek(0)
                file_reader = []
                csv_reader = csv.reader(data_file, delimiter=',')
            except Exception:
                raise exceptions.Warning(_("Please upload csv file !"))
            try:
                file_reader.extend(csv_reader)
            except Exception:
                raise exceptions.Warning(_("Invalid file!"))
            values = {}
            for i in range(len(file_reader)):
                field = list(map(str, file_reader[i]))
                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        res = self.create_sale_order_line(values)
        else:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            try:
                fp.write(binascii.a2b_base64(self.order_line_file))
                fp.seek(0)
                values = {}
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
            except Exception:
                raise exceptions.Warning(_("Please upload xlsx file !"))
            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    get_line = list(map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    if self.product_select_option == 'from_product':
                        values.update({'product': get_line[0], 'quantity': get_line[1]})
                    else:
                        values.update({
                            'product': get_line[0],
                            'quantity': get_line[1],
                            'uom': get_line[2],
                            'description': get_line[3],
                            'price': get_line[4],
                            'tax': get_line[5],
                        })
                    res = self.create_sale_order_line(values)
        return res

    def create_sale_order_line(self, values):
        sale_order_brw = self.env['sale.order'].browse(self._context.get('active_id'))
        product = values.get('product')
        if self.product_select_option == 'from_product':
            if self.import_product_option == 'barcode':
                product_obj_search = self.env['product.product'].search([('barcode', '=', values['product'])], limit=1)
            elif self.import_product_option == 'code':
                product_obj_search = self.env['product.product'].search([('default_code', '=', values['product'])], limit=1)
            else:
                product_obj_search = self.env['product.product'].search([('name', '=', values['product'])], limit=1)

            if product_obj_search:
                product_id = product_obj_search
            else:
                raise Warning(_('%s product not available in Product master ".') % values.get('product'))

            if sale_order_brw.state == 'draft':
                self.env['sale.order.line'].create({
                    'order_id': sale_order_brw.id,
                    'product_id': product_id.id,
                    'name': product_id.name,
                    'product_uom_qty': values.get('quantity'),
                    'product_uom': product_id.uom_id.id,
                    'price_unit': product_id.lst_price,
                })
            elif sale_order_brw.state == 'sent':
                self.env['sale.order.line'].create({
                    'order_id': sale_order_brw.id,
                    'product_id': product_id.id,
                    'name': product_id.name,
                    'product_uom_qty': values.get('quantity'),
                    'product_uom': product_id.uom_id.id,
                    'price_unit': product_id.lst_price,
                })
            elif sale_order_brw.state != 'sent' or sale_order_brw.state != 'draft':
                raise UserError(_('We cannot import data in validated or confirmed order.'))
        else:
            uom = values.get('uom')
            if self.import_product_option == 'barcode':
                product_obj_search = self.env['product.product'].search([('barcode', '=', values['product'])], limit=1)
            elif self.import_product_option == 'code':
                product_obj_search = self.env['product.product'].search([('default_code', '=', values['product'])], limit=1)
            else:
                product_obj_search = self.env['product.product'].search([('name', '=', values['product'])], limit=1)

            uom_obj_search = self.env['uom.uom'].search([('name', '=', uom)], limit=1)
            tax_id_lst = []
            if values.get('tax'):
                if ';' in values.get('tax'):
                    tax_names = values.get('tax').split(';')
                    for name in tax_names:
                        tax = self.env['account.tax'].search([('name', '=', name), ('type_tax_use', '=', 'sale')], limit=1)
                        if not tax:
                            raise Warning(_('"%s" Tax not Present ') % name)
                        tax_id_lst.append(tax.id)

                elif ',' in values.get('tax'):
                    tax_names = values.get('tax').split(',')
                    for name in tax_names:
                        tax = self.env['account.tax'].search([('name', '=', name), ('type_tax_use', '=', 'sale')], limit=1)
                        if not tax:
                            raise Warning(_('"%s" Tax not Present') % name)
                        tax_id_lst.append(tax.id)
                else:
                    tax_names = values.get('tax').split(',')
                    tax = self.env['account.tax'].search([('name', '=', tax_names), ('type_tax_use', '=', 'sale')], limit=1)
                    if not tax:
                        raise Warning(_('"%s" Tax not Present') % tax_names)
                    tax_id_lst.append(tax.id)

            if not uom_obj_search:
                raise Warning(_('UOM "%s"  Not Present') % uom)

            if product_obj_search:
                product_id = product_obj_search
            else:
                raise Warning(_('%s product not available in Product master ".') % values.get('product'))

            if sale_order_brw.state == 'draft':
                order_lines = self.env['sale.order.line'].create({
                    'order_id': sale_order_brw.id,
                    'product_id': product_id.id,
                    'name': values.get('description'),
                    'product_uom_qty': values.get('quantity'),
                    'product_uom': uom_obj_search.id,
                    'price_unit': values.get('price'),
                })
            elif sale_order_brw.state == 'sent':
                order_lines = self.env['sale.order.line'].create({
                    'order_id': sale_order_brw.id,
                    'product_id': product_id.id,
                    'name': values.get('description'),
                    'product_uom_qty': values.get('quantity'),
                    'product_uom': uom_obj_search.id,
                    'price_unit': values.get('price'),
                })
            elif sale_order_brw.state != 'sent' or sale_order_brw.state != 'draft':
                raise UserError(_('you cannot import invalid data or confirmed order.'))
            if tax_id_lst:
                order_lines.write({'tax_id': ([(6, 0, tax_id_lst)])})
        return True
