# -*- coding: utf-8 -*-
from odoo import models, fields, api
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


class biproductgeneratebarcodemanually(models.TransientModel):
    _name = 'bi.product.generate.barcode.manually'

    generate_type = fields.Selection([('reference', 'Using Internal Reference'), ('random', 'Using Random Number')],
                                       string='Barcode Generate Option', default='reference')

    def generate_barcode_manually(self):
        for record in self.env['product.product'].browse(self._context.get('active_id')):
            record.set_product_barcode(self.generate_type)
        return True
        

class bi_generate_product_barcode(models.TransientModel):
    _name = 'bi.product.generate.barcode'

    overwrite= fields.Boolean(String="Overwrite Exists Ean13")
    generate_type = fields.Selection([('reference', 'Using Internal Reference'), ('random', 'Using Random Number')],
                                       string='Barcode Generate Option', default='reference')


    def generate_barcode(self):
        for record in self.env['product.product'].browse(self._context.get('active_ids')):
            record.set_product_barcode(self.generate_type)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
