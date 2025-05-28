from odoo import models, fields

class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'
    
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
 