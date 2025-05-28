from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_brand = fields.Char(compute='_compute_product_brand')
    product_brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
        related='product_id.product_tmpl_id.brand_id',
        store=True,
        readonly=True
    )
    payment_type = fields.Selection(
        related='order_id.payment_type',
        string='Payment Type',
        store=True,
        readonly=True
    )

    @api.depends('product_id')
    def _compute_product_brand(self):
        for line in self:
            # Example: get the product brand from the product_id's brand field
            line.product_brand_id = line.product_id.product_brand_id.name if line.product_id else False
