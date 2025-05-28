{
    'name': 'Custom Form',
    'version': '1.0',
    'depends': ['base','sale','web'],
    'category': 'Custom',
    'summary': 'Custom Form for Customers',
    'description': 'This is a custom module for managing customers.',
    'author': 'Shalom Hosheya',
    'application': True,  # <-- THIS IS VERY IMPORTANT
    'data': [
        'security/ir.model.access.csv',
        'views/cf_receipt_views.xml',
        'views/customer_view.xml',
        'report/customer_receipt_report.xml',
        'views/cf_receipt_template.xml',
        # 'views/report_layout.xml',
        'views/action.xml',
        'views/menu.xml',
        
    ],
    'installable':True
}
