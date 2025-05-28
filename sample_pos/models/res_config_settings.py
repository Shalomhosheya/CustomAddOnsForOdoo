from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_picking_policy = fields.Selection([
        ('direct', 'Ship Directly'),
        ('one', 'Group All Deliveries')
    ], string="Default Picking Policy", default='direct')
