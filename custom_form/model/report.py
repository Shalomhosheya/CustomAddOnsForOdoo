from odoo import models

class CustomerReceiptReport(models.AbstractModel):
    _name = 'report.custom_form.customer_receipt_template'
    _description = 'Customer Receipt Report'
    
    def _get_report_values(self, docids, data=None):
        docs = self.env['cf.receipt'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'cf.receipt',
            'docs': docs,
        }