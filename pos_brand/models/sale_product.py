from odoo import models, fields

class SaleProduct(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Brand', required=True)