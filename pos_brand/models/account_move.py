# models/account_move.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from lxml import etree

class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_type = fields.Selection(
        [('cash', 'Cash'), ('card', 'Card')],
        string='Payment Type',
        readonly=True,
        store=True
    )

    @api.onchange('invoice_origin')
    def _compute_payment_type_from_origin(self):
        for move in self:
            if move.invoice_origin:
                sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
                if sale_order:
                    move.payment_type = sale_order.payment_type

    @api.model
    def _get_sequence_prefix(self):
        """Return the sequence prefix based on payment type."""
        if self.payment_type == 'card':
            return 'INVS/%(year)s/'
        return 'INV/%(year)s/'

    @api.model
    def _get_sequence(self):
        """Override to dynamically select or create a sequence based on payment type."""
        self.ensure_one()
        if self.move_type != 'out_invoice' or not self.payment_type:
            return super(AccountMove, self)._get_sequence()

        sequence_code = f'account.invoice.{self.payment_type}'
        sequence = self.env['ir.sequence'].search([
            ('code', '=', sequence_code),
            ('company_id', 'in', [self.company_id.id, False])
        ], limit=1)

        if not sequence:
            prefix = self._get_sequence_prefix()
            sequence = self.env['ir.sequence'].create({
                'name': f'Customer Invoice - {self.payment_type.title()}',
                'code': sequence_code,
                'prefix': prefix,
                'padding': 5,
                'company_id': self.company_id.id,
                'number_increment': 1,
                'number_next_actual': 1,
            })
        return sequence

    def _set_next_sequence(self):
        """Override to set the next sequence number based on payment type."""
        self.ensure_one()
        if self.move_type == 'out_invoice' and self.payment_type:
            sequence = self._get_sequence()
            if sequence:
                next_number = sequence.with_context(
                    ir_sequence_date=self.date,
                    ir_sequence_date_range=self.date
                ).next_by_id()
                while self.env['account.move'].search([
                    ('name', '=', next_number),
                    ('journal_id', '=', self.journal_id.id)
                ]):
                    sequence.number_next_actual += 1
                    next_number = sequence.with_context(
                        ir_sequence_date=self.date,
                        ir_sequence_date_range=self.date
                    ).next_by_id()
                self.name = next_number
            else:
                raise UserError(_("No sequence found for the invoice."))
        else:
            super(AccountMove, self)._set_next_sequence()

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """Restrict payment_type to 'Cash' for non-admin users in the UI."""
        res = super(AccountMove, self).fields_view_get(view_id, view_type, toolbar, submenu)

        if view_type == 'form' and not self.env.user.has_group('base.group_system'):
            doc = etree.XML(res['arch'])

            for node in doc.xpath("//field[@name='payment_type']"):
                node.set('readonly', '1')
                node.set('default', 'cash')

            res['arch'] = etree.tostring(doc, encoding='unicode')

            if 'fields' in res and 'payment_type' in res['fields']:
                res['fields']['payment_type']['selection'] = [('cash', 'Cash')]

        return res

    @api.model
    def create(self, vals):
        """Allow all users to create invoices with any payment type."""
        if 'payment_type' not in vals:
            vals['payment_type'] = 'cash'
        return super(AccountMove, self).create(vals)

    def write(self, vals):
        """Allow all users to edit invoices with any payment type."""
        return super(AccountMove, self).write(vals)
