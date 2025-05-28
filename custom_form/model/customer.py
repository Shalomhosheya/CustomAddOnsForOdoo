from odoo import models, fields, api

class CFCustomer(models.Model):
    _name = 'cf.customer'
    _description = 'Custom Form Customer'
    
    customercode = fields.Char(string='Customer Code')
    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    size = fields.Char(string='Size')
    
    def action_confirm(self):
        # This method will be called when button is clicked
        # Generate receipt logic here
        receipt = self.env['cf.receipt'].create({
            'customer_code': self.customercode,
            'customer_name': self.name,
            'date': self.date,
            'size': self.size,
        })
        
        # Return action to show the receipt
        return {
            'name': 'Customer Receipt',
            'type': 'ir.actions.act_window',
            'res_model': 'cf.receipt',
            'view_mode': 'form',
            'res_id': receipt.id,
            'target': 'new',
        }