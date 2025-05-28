{
    'name': 'POS Custom Notes',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Add custom notes to POS orders',
    'description': """
        This module extends Point of Sale functionality to:
        - Add custom notes to orders
        - Display notes on receipts
        - Track special customer requests
    """,
    'author': 'Shalom Hosheya',
    'website': 'https://yourwebsite.com',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'stock'],
    
    'data': [
        'security/ir.model.access.csv',
        # 'views/view_pos_order_tree.xml',
        # 'views/action.xml',               # Ensure this file exists
        # 'views/menu.xml',                 # Ensure this file exists
        # 'views/pos_custom_view.xml',      # Ensure this file exists
    ],

    'assets': {
        # 'point_of_sale.assets': [
        #     'pos_custom/static/src/js/pos_custom.js',
        #     'pos_custom/static/src/xml/pos_custom_templates.xml',
        #     'pos_custom/static/src/css/pos_custom.css',
        # ],
    },
    
    'demo': [],  # Add demo data if available or leave it empty

    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 0.00,
    'currency': 'USD',
}
