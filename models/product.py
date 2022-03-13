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
import logging

_logger = logging.getLogger(__name__)

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
        if vals:
            option = self.env['ir.config_parameter'].sudo().get_param('bi_generate_product_ean13.generate_option')
            if not vals.get('barcode') and option:
                _logger.info(vals)
                barcode_vals = self.set_product_barcode(option, reference_code=vals.get('default_code'))
                vals.update(barcode_vals)
                _logger.info(vals)
                
        return super(productproduct, self).create(vals)
    
    def set_product_barcode(self, option, reference_code=None):
        
        reference_code = reference_code or self.default_code
        if option == 'reference':
            if not reference_code:
                raise UserError(f'You have set to automatically generate barcode on product creation using the internal reference. \
                                However missing internal reference of product. {reference_code}')
            
            if len(reference_code) > 5:
                raise UserError(f'EAN13 supports only five digit for product. Please provide max five digit internal reference: {reference_code}')
            
        else:
            reference_code = int("%0.5d" % random.randint(0, 99999))
        
        AMOUNT = "00000" # Amount in decimal NNNDD
        ean_barcode = BARCODE_PREFIX + str(reference_code).zfill(5) + AMOUNT
        ean_barcode = self.env['barcode.nomenclature'].sanitize_ean("%s" % (ean_barcode))
        imgdata = self.generate_barcode_image(ean_barcode)
        vals = {'default_code': reference_code, 'barcode': ean_barcode, 'barcode_img': imgdata}
        self.write(vals)
        return vals

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
