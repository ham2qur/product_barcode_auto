# -*- coding: utf-8 -*-
{
    'name': 'Product Barcode Auto (EAN13)',
    'version': '14.0.0.2',
    'summary': "Generate EAN13 barcode based on internal reference. EAN13 supports product quanity using barcode nomenclature.",
    'category': 'Sales',
    'description': """
""",
    'author': 'ham2qur',
    'website': 'http://www.tradetec.info',
    'depends': ['base', 'product', 'sale', 'barcodes','sale_management', 'bi_dynamic_barcode_labels'],
    'data': [
        'security/ir.model.access.csv',
        'views/generate_product_ean13_view.xml',
        'views/res_config_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
