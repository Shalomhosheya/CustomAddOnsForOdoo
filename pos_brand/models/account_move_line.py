from odoo import models, fields 

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    product_brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
        related='product_id.product_tmpl_id.brand_id',
        store=True,
        readonly=True
    )
    
    payment_type = fields.Selection(
        related='move_id.payment_type',
        string='Payment Type',
        store=True,
        readonly=True
    )
