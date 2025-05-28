from odoo import models, fields

class PosOrder(models.Model):
    _inherit = 'pos.order'

    custom_note = fields.Text(string='Custom Note')

    # Optional: you can create a setter method to update the custom_note
    def set_custom_note(self, note):
        self.custom_note = note
        self.save()
