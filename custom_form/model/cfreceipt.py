from odoo import models, fields
from odoo.exceptions import UserError

class CFReceipt(models.Model):
    _name = 'cf.receipt'
    _description = 'Customer Receipt'
    
    customer_code = fields.Char(string='Customer Code', readonly=True)
    customer_name = fields.Char(string='Customer Name', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    size = fields.Char(string='Size', readonly=True)

     
    def print_receipt(self):
     try:
        report = self.env.ref('custom_form.customer_receipt_report')
        return report.report_action(self)
     except Exception as e:
        raise UserError(f"Failed to print receipt: {str(e)}")
