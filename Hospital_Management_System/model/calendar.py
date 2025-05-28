from odoo import models, fields, api

class HospitalAppointmentCalendar(models.Model):
    _inherit = 'calendar.event'

    appointment_id = fields.Many2one('hospital_management_system.appointment', string="Appointment", ondelete='cascade')
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    reference = fields.Char(string="Reference")

    @api.model
    def create(self, vals):
        # Optionally sync with appointment
        if 'appointment_id' in vals:
            appointment = self.env['hospital_management_system.appointment'].browse(vals['appointment_id'])
            vals['name'] = f"Appointment: {appointment.reference}"
            vals['start'] = appointment.date_appointment
            vals['stop'] = appointment.date_appointment  # Add duration logic if needed
        return super().create(vals)
