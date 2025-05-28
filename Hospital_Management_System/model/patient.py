from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hospital_management_system.patient' 
    _inherit = ['mail.thread']
    _description = 'Hospital Patient'
    
    
    name = fields.Char(string='Name', required=True,tracking=True)
    age = fields.Integer(string='Age',tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender',tracking=True)
    
    email = fields.Char(string='Email',tracking=True)
    phone_number = fields.Char(string="Phone Number")  # <== check this exact field name
    address = fields.Text(string="Address")
    image = fields.Binary(string="Image")
    nic_number = fields.Char(string="NIC Number")
    tag_ids = fields.Many2many('patient.tag','patient_tag_rel','patient_id','tag_id' ,string='Tags')
    