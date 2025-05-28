from odoo import models, fields

class Patient(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'
    _order = 'sequence, id' 

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence')
