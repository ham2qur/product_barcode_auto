# -*- coding: utf-8 -*-
from odoo import models, api,fields, _
from datetime import datetime
import random
import barcode
try:
    from barcode.writer import ImageWriter
except ImportError:
    ImageWriter = None  # lint:ok
import base64
import os
from odoo.exceptions import UserError

BARCODE_PREFIX = "21"

class productproduct(models.Model):
    _inherit = "product.product"

    check_barcode_setting = fields.Boolean('Check Barcode Setting')
    barcode_img = fields.Binary('Barcode Image')
    
    @api.model
    def default_get(self, field_lst):
        res = super(productproduct, self).default_get(field_lst)
        if not self.env['ir.config_parameter'].sudo().get_param('bi_generate_product_ean13.gen_barcode'):
            res['check_barcode_setting'] = True
        return res



    @api.model
    def create(self, vals):
        res = super(productproduct, self).create(vals)
        if res:
            option = self.env['ir.config_parameter'].sudo().get_param('bi_generate_product_ean13.generate_option')
            if not vals.get('barcode') and option:
                self.set_product_barcode(option)

        return res
    
    def set_product_barcode(self, option):
        
        bcode = None
        if option == 'reference':
            bcode = self.default_code
            if not bcode:
                raise UserError(f'Missing internal reference of product: {self.name}')
            
            if len(bcode) > 5:
                raise UserError(f'EAN13 supports only five digit for product. Please provide max five digit internal reference: {self.default_code}')
            
        else:
            bcode = int("%0.5d" % random.randint(0, 99999))
        
        bcode = BARCODE_PREFIX + str(bcode).zfill(5) + "00000"
        bcode = self.env['barcode.nomenclature'].sanitize_ean("%s" % (bcode))
        imgdata = self.generate_barcode_image(bcode)
        self.write({'barcode' : bcode, 'barcode_img': imgdata})

    def generate_barcode_image(self, code):
        
        ean = barcode.get('ean13', code, writer=ImageWriter())
#                 path  =  os.path.abspath('bi_generate_product_ean13')
        filename = ean.save('/tmp/ean13')
        f = open(filename, 'rb')
        jpgdata = f.read()
        imgdata = base64.encodestring(jpgdata)
        os.remove(filename)
        return imgdata
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
