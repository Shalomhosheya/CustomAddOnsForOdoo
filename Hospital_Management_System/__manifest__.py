{
    'name': 'MediCare Hospital Management System',
    'version': '1.0',
    'summary': 'Manage hospital Patients Appointments and Receipts',
    'category': 'Tools',
    'description': 'Hospital management system',
    'author': 'Shalom Hosheya',
    'depends': ['base', 'mail','calendar','product','account'],
    'data': [
    'security/ir.model.access.csv',
    'views/report_receipt_template.xml', 
    'report/report.xml', 
    'data/sequence.xml', 
    'views/patients_readonly.xml',
    'views/calendar_view.xml',
    'views/patients_view.xml',
    'views/patients_tag_view.xml', 
    'views/appointment_view.xml',                
    'views/menu.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
