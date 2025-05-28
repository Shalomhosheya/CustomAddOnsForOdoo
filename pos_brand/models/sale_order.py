from odoo import models, fields, api
from lxml import etree

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_note = fields.Char(string='Custom Note')

    payment_type = fields.Selection(
        [('cash', 'Cash'), ('card', 'Card')],
        string='Payment Type'
    )

    invoice_type = fields.Selection(
        [('cash', 'Cash'), ('card', 'Card'), ('none', 'No Invoice')],
        string="Invoice Type",
        compute="_compute_invoice_type",
        store=True,
        index=True
    )

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super()._create_invoices(grouped=grouped, final=final, date=date)

        for order in self:
            related_invoices = invoices.filtered(lambda inv: inv.invoice_origin == order.name)
            for invoice in related_invoices:
                if order.payment_type == 'cash':
                    sequence = self.env['ir.sequence'].next_by_code('account.move.invoice.cash')
                    invoice.name = sequence
                elif order.payment_type == 'card':
                    sequence = self.env['ir.sequence'].next_by_code('account.move.invoice.card')
                    invoice.name = sequence

        return invoices

    def _get_dashboard_data(self):
        res = super()._get_dashboard_data()
        user = self.env.user

        if not user.has_group('account.group_account_manager'):
            res['nb_invoice_to_validate'] = 0
            res['amount_invoice_to_validate'] = 0.0

        return res

    @api.depends('invoice_ids', 'invoice_ids.name')
    def _compute_invoice_type(self):
        for order in self:
            invoice_names = order.invoice_ids.mapped('name')
            if not invoice_names:
                order.invoice_type = 'none'
            elif any(name.startswith('INVS/') for name in invoice_names):
                order.invoice_type = 'card'
            elif any(name.startswith('INV/') for name in invoice_names):
                order.invoice_type = 'cash'
            else:
                order.invoice_type = 'none'

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals['payment_type'] = self.payment_type or 'cash'
        return invoice_vals

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)
        user = self.env.user
        is_admin = user.has_group('base.group_system') or user.has_group('sales_team.group_sale_manager')

        if not is_admin and view_type in ['form', 'tree']:
            if 'fields' in res and 'payment_type' in res['fields']:
                res['fields']['payment_type']['selection'] = [('cash', 'Cash')]

            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//field[@name='payment_type']"):
                    node.set('default', 'cash')
                res['arch'] = etree.tostring(doc, encoding='unicode')

        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        user = self.env.user
        is_admin = user.has_group('base.group_system') or user.has_group('sales_team.group_sale_manager')

        if not is_admin:
            cash_domain = [('payment_type', 'in', ['cash', False])]
            domain = cash_domain + (domain or [])

        return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    @api.model
    def web_search_read(self, domain=None, specification=None, offset=0, limit=None, order=None, count_limit=None):
        user = self.env.user
        is_admin = user.has_group('base.group_system') or user.has_group('sales_team.group_sale_manager')

        if not is_admin:
            cash_domain = [('payment_type', 'in', ['cash', False])]
            domain = cash_domain + (domain or [])

        return super().web_search_read(
            domain=domain,
            specification=specification,
            offset=offset,
            limit=limit,
            order=order,
            count_limit=count_limit
        )
