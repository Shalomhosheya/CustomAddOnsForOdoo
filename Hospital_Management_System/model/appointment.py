from odoo import models, fields, api
from datetime import timedelta 
class HospitalAppointment(models.Model):
    _name = 'hospital_management_system.appointment' 
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id'
    _order = 'sequence, id'  # Add this only if you're using `sequence`
    amount_paid = fields.Monetary(string='Amount Paid')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    sequence = fields.Integer(string="Sequence", default=10) 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], tracking=True, default='draft')
    
    reference = fields.Char(string='Reference', default='New', required=True, tracking=True)
    patient_id = fields.Many2one('hospital_management_system.patient', string='Patient', required=True, tracking=True)
    date_appointment = fields.Datetime(string='Appointment Date & Time', required=True, tracking=True)
    duration = fields.Float(string='Duration (Hours)', default=1.0)
    note = fields.Text(string='Note')
    end_datetime = fields.Datetime(string='End Date & Time', compute='_compute_end_datetime', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital_management_system.appointment') or 'New'
        return super().create(vals_list)
    

    @api.depends('date_appointment', 'duration')
    def _compute_end_datetime(self):
        for record in self:
            if record.date_appointment:
                record.end_datetime = record.date_appointment + timedelta(hours=record.duration)
            else:
                record.end_datetime = False

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_ongoing(self):
        for record in self:
            record.state = 'ongoing'
            
    def action_done(self):
        for record in self:
            record.state = 'done'
            
    def action_cancel(self):
        for record in self:
            record.state = 'cancel'
            
    def action_draft(self):
        for record in self:
            record.state = 'draft'


    def action_generate_receipt(self):
        return self.env.ref('your_module.report_receipt_action').report_action(self)
    
    def action_print_receipt(self):
       return self.env.ref('hospital_management_system.report_appointment_receipt_template').report_action(self)