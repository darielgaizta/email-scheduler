from unittest.mock import patch, MagicMock
from app.services.email import send_email, save_email, check_scheduled_emails_task
from datetime import datetime

@patch('app.services.email.Email')
def test_save_email(mock_email):
    mock_email_instance = MagicMock()
    mock_email.return_value = mock_email_instance

    result = save_email(
        event_id=1,
        subject="Test Subject",
        content="Hello world",
        timestamp="2025-08-12 10:00:00",
        recipients='a@example.com; b@example.com'
    )

    mock_email.assert_called_once_with(
        event_id=1,
        subject="Test Subject",
        content="Hello world",
        timestamp="2025-08-12 10:00:00",
        recipients='a@example.com; b@example.com'
    )
    mock_email_instance.create.assert_called_once()

    assert result == mock_email_instance
    assert result.event_id == mock_email_instance.event_id
    assert result.subject == mock_email_instance.subject
    assert result.content == mock_email_instance.content


def test_send_email(app):
    with patch('app.services.email.EmailMessage.send') as mock_send:
        mock_send.return_value = True
        app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'

        with app.app_context():
            result = send_email(
                subject='Test Subject',
                content='Hello world',
                recipients='a@example.com; b@example.com'
            )
        mock_send.assert_called_once()
        assert result == 'Email with subject "Test Subject" has been sent to a@example.com; b@example.com.'


def test_check_scheduled_emails(monkeypatch, app):
    fake_now = datetime(2025, 8, 12, 10, 0)

    class FakeEmail:
        timestamp = fake_now
        is_sent = False
        subject = "Test Subject"
        content = "Hello world"
        recipients = "a@example.com; b@example.com"

        def update(self, **kwargs):
            self.is_sent = kwargs['is_sent']

    class MockQuery:
        def filter(self, *args, **kwargs):
            return self
        
        def all(self):
            return [FakeEmail()]

    class MockEmail:
        query = MockQuery()
        timestamp = FakeEmail.timestamp
        is_sent = FakeEmail.is_sent

    class MockNow:
        def replace(self, *args, **kwargs):
            return fake_now

    class MockDatetime:
        now = lambda: MockNow()

    with app.app_context():
        monkeypatch.setattr('app.services.email.Email', MockEmail)
        monkeypatch.setattr('app.services.email.datetime', MockDatetime)
        monkeypatch.setattr('app.services.email.send_email.delay', MagicMock())
        result = check_scheduled_emails_task()
    assert "1 email(s) were added to the queue for sending." in result
