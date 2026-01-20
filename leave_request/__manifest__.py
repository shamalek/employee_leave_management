{
    'name': 'leave_request',
    'category': 'hr',
    'sequence': 5,
    'summary': 'Centralize your address book',
    'description': """
This module gives you a quick view of your contacts directory, accessible from your home page.
You can track your vendors, customers and other contacts.
""",
    'depends': ['hr'],
    'data': [
        "security/ir.model.access.csv",
        "security/leave_request_rules.xml",
        "views/leave_req.xml"
    ],
    'demo': [

    ],
    'application': True,
    'license': 'LGPL-3',
}
