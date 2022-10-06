# -*- coding: utf-8 -*-
import base64
from io import BytesIO

import qrcode as qrcode

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _


class VandorRestaurant(models.Model):
    _name = "vendor.restaurant"
    _description = "Vendor Restaurant"

    name = fields.Char(string="Name")
    vendor_id = fields.Many2one('res.partner', string="Vendor")
    image = fields.Image('Banner')
    logo = fields.Image('Logo')
    category_line_ids = fields.One2many('vendor.restaurant.category', 'restaurant_ids', string='Category  Lines')
    url = fields.Char(compute="_get_url")
    short_name = fields.Char(compute="_get_url")
    qr_code = fields.Char(string="QR Code", related="url")
    qr_image = fields.Binary(string="QR", compute="_generate_qr_code")
# fields for contacts
    contact_image = fields.Image('Contact US', required=True)
    contact_name = fields.Char(string="Contact Name")
    contact_url = fields.Char(string="our contact", compute="_get_url")
    restaurant_contact_line = fields.One2many('vendor.restaurant.contact', 'rest_contact_id', string='Contacts Lines')
# fields added for user id
    user_name = fields.Char(string="User Name")
    email = fields.Char(string="Email")
    password = fields.Char(string="Password")
    user_id = fields.Many2one('res.users',string='user')

     # fields added for social links
    face_book = fields.Char(string='FaceBook')
    instagram = fields.Char(string="Instagram")

    # actions
    @api.constrains('name')
    def check_similar_name(self):
        for rec in self:
            name = self.env['vendor.restaurant'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if name:
                raise ValidationError(_("Restaurant name %s already exists." % rec.name))

    @api.model
    def create(self, vals):
        res = super(VandorRestaurant, self).create(vals)
        print('hellow world this is me................')
        user = self.env['res.users'].create({
            'login': vals.get('email'),
            'email': vals.get('email'),
            'name': vals.get('user_name'),
            'password': vals.get('password'),
            'company_id': self.env.company.id,
            'groups_id': [(6, 0, self.env.ref('om_menu.group_restaurant_read_write'))],
        })
        return res

    # @api.model
    # def create(self, vals):
    #
    #     res = super(VandorRestaurant, self).create(vals)
    #     print('vals....', vals)
    #     user_record = {
    #         'name': self.name,
    #         'email': self.email,
    #         'password': self.password,
    #     }
    #     print('user record', user_record)
    #     self.env['res.users'].create(user_record)
    #
    #     return res

    def _generate_qr_code(self):
        if self.qr_code:
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20,
                               border=4)
            qr.add_data(self.qr_code)
            qr.make(fit=True)
            img = qr.make_image()
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qrcode_img = base64.b64encode(buffer.getvalue())
            self.qr_image = qrcode_img
        else:
            self.qr_image = False

    def _get_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.url = base_url + '/om-menu' + '/' + self.name.replace(' ', '-').lower()
        self.contact_url = base_url + '/om-menu/contactus/' + '/' + self.name.replace(' ', '-').lower()
        self.short_name = self.name.replace(' ', '-').lower()


class RestaurantCategory(models.Model):
    _name = "vendor.restaurant.category"
    _description = "Vendor Restaurant Category"

    name = fields.Char(string="Name")
    image = fields.Image('Image')
    restaurant_product_line = fields.One2many('vendor.restaurant.product', 'category_id', string='Product Lines')
    restaurant_ids = fields.Many2one('vendor.restaurant', string='Restaurant Ids')

class RestaurantProduct(models.Model):
    _name = "vendor.restaurant.product"
    _description = "Vendor Restaurant Products"

    name = fields.Char(string="Name")
    arabic_name = fields.Char(string="Arabic Name")
    image = fields.Image('Image')
    category_id = fields.Many2one('vendor.restaurant.category')
    price = fields.Float()
    size = fields.Char()
    arabic_size = fields.Char(string="Size In Arabic")
    ingredients = fields.Char()
    arabic_ingredients = fields.Char(string="Ingredients in Arabic")
    description = fields.Text(string="Description")
    # link = fields.Many2one('vendor.restaurant')

class RestaurantContactUs(models.Model):
    _name = "vendor.restaurant.contact"
    _description = "Vendor Restaurant Contact"

    name = fields.Char(string="Branch Name")
    phone = fields.Char(string="Phone Number")
    location = fields.Char(string="Location")
    rest_contact_id = fields.Many2one('vendor.restaurant', string='Restaurant Contact')




