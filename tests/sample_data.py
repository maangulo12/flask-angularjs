#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    sample_data.py
    ---------------

    This module is used for adding sample data to the database.

    -How to use it (type the following in the command-line):
        python3 manage.py populate
"""

import random
import simplejson as json

from app.utility import parse_ubuildit_file, parse_invoice_file


FILE_PATH = 'tests/data/spreadsheet.xlsx'


def populate_db(app):
    # Client test
    app.testing = True
    client = app.test_client()

    # Create User
    client.post('/api/users', data=json.dumps({
        'username':   'test',
        'password':   'test',
        'first_name': 'test',
        'last_name':  'test',
        'email':      'test@gmail.com'
    }),
        headers={
        'Content-Type': 'application/json'
    })

    # Authenticate User
    response = client.post('/api/auth', data=json.dumps({
        'login':    'test',
        'password': 'test'
    }),
        headers={
        'Content-Type': 'application/json'
    })

    # Auth Token
    data = json.loads(response.data.decode('utf-8'))
    token = data['token']

    # Create Project
    client.post('/api/projects', data=json.dumps({
        'name':         'UBuildIt - Tim & Maritza Messer',
        'address':      '251 Wizard Way',
        'city':         'Spring Branch',
        'state':        'TX',
        'zipcode':      '78070',
        'home_sq':      '2000',
        'project_type': 'ubuildit',
        'user_id':      1
    }),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })

    # Start parsing UBUILDIT file here
    data = parse_ubuildit_file(FILE_PATH)

    for category in data:
        # Add Category
        client.post('/api/categories', data=json.dumps({
            'name':       category['category_name'],
            'project_id': 1
        }),
            headers={
            'Content-Type':  'application/json',
            'Authorization': 'Bearer ' + token
        })

        for item in category['item_list']:
            # Add Item
            client.post('/api/items', data=json.dumps({
                'name':        item['cost_category'],
                'description': item['description'],
                'estimated':   item['estimated'],
                'actual':      item['actual'],
                'category_id': data.index(category) + 1,
                'project_id':  1
            }),
                headers={
                'Content-Type':  'application/json',
                'Authorization': 'Bearer ' + token
            })

    # Add Funds/Loans
    client.post('/api/funds', data=json.dumps({
        'name':       'Messer',
        'loan':       False,
        'amount':     100000.00,
        'project_id': 1
    }, use_decimal=True),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })
    client.post('/api/funds', data=json.dumps({
        'name':       'Blanco Loan',
        'loan':       True,
        'amount':     330000.00,
        'project_id': 1
    }, use_decimal=True),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })

    # Add Draws
    client.post('/api/draws', data=json.dumps({
        'date':    '09/24/2015',
        'amount':  25000.00,
        'fund_id': 2
    }, use_decimal=True),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })
    client.post('/api/draws', data=json.dumps({
        'date':    '10/01/2015',
        'amount':  5000.00,
        'fund_id': 2
    }, use_decimal=True),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })
    client.post('/api/draws', data=json.dumps({
        'date':    '10/03/2015',
        'amount':  7500.00,
        'fund_id': 2
    }, use_decimal=True),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })

    # Start parsing INVOICE file here
    data = parse_invoice_file(FILE_PATH)
    for expenditure in data:
        fund_id = 1
        if expenditure['notes'] == 'Blanco':
            fund_id = 2

        client.post('/api/expenditures', data=json.dumps({
            'date':        expenditure['date'],
            'vendor':      expenditure['vendor'],
            'notes':       expenditure['description'],
            'cost':        expenditure['cost'],
            'category_id': random.randint(1, 8),
            'item_id':     random.randint(1, 110),
            'fund_id':     fund_id,
            'project_id':  1
        }, use_decimal=True),
            headers={
            'Content-Type':  'application/json',
            'Authorization': 'Bearer ' + token
        })

    # Add Subcontractors
    client.post('/api/subcontractors', data=json.dumps({
        'name':           'John Smith',
        'company':        '84 Lumber',
        'contact_number': '210-543-4534',
        'project_id':     1
    }),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })
    client.post('/api/subcontractors', data=json.dumps({
        'name':           'Shawn Tarver',
        'company':        'Ez Company',
        'contact_number': '512-586-6516',
        'project_id':     1
    }),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })
    client.post('/api/subcontractors', data=json.dumps({
        'name':           'Mike Jones',
        'company':        'Coca Cola',
        'contact_number': '210-253-5861',
        'project_id':     1
    }),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })
    client.post('/api/subcontractors', data=json.dumps({
        'name':           'Alex Ramirez',
        'company':        'Rusty Corp',
        'contact_number': '256-645-7854',
        'project_id':     1
    }),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })
    client.post('/api/subcontractors', data=json.dumps({
        'name':           'Nick Ross',
        'company':        'AAA Company',
        'contact_number': '123-454-3443',
        'project_id':     1
    }),
        headers={
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + token
    })
