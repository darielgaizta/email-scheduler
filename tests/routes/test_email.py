def test_form_page(client):
    response = client.get('/save_emails')
    assert response.status_code == 200
    assert b'Send Email' in response.data

def test_form_validation(client):
    response = client.post('/save_emails', data={
        'event_id': '1',
        'subject': 'MySubject',
        'content': 'MyContent',
        'timestamp': '12 Aug 2025 15:30',
        'recipients': 'fatihdarielma@gmail.com; darielgaizta@gmail.com'
    })
    assert response.status_code == 200

def test_form_invalid_email(client):
    response = client.post('/save_emails', data={
        'event_id': '1',
        'subject': 'MySubject',
        'content': 'MyContent',
        'timestamp': '12 Aug 2025 15:30',
        'recipients': '-+john.doe@gmail.com;=lorem.ipsum@google.co.id;?hello_world01@yahoo.co.uk'
    })
    assert response.status_code == 200
    assert b'Invalid email address' in response.data

def test_form_invalid_event_id(client):
    response = client.post('/save_emails', data={
        'event_id': '0',
        'subject': 'MySubject',
        'content': 'MyContent',
        'timestamp': '12 Aug 2025 15:30',
        'recipients': 'john.doe@gmail.com; lorem.ipsum@google.co.id; hello_world01@yahoo.co.uk'
    })
    assert response.status_code == 200
    assert b'Event ID must be greater than 0.' in response.data

def test_form_invalid_timestamp(client):
    response = client.post('/save_emails', data={
        'event_id': '1',
        'subject': 'MySubject',
        'content': 'MyContent',
        'timestamp': 'invalid-timestamp',
        'recipients': 'john.doe@gmail.com; lorem.ipsum@google.co.id; hello_world01@yahoo.co.uk'
    })
    assert response.status_code == 200
    assert b'Not a valid datetime value.' in response.data

def test_form_missing_data(client):
    response = client.post('/save_emails', data={
        'event_id': '',
        'subject': '',
        'content': '',
        'timestamp': '',
        'recipients': ''
    })
    assert response.status_code == 200
    assert b'This field is required.' in response.data