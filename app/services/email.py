from celery import shared_task
from flask_mailman import EmailMessage
from flask import current_app

from app.models.email import Email
from datetime import datetime

def save_email(event_id, subject, content, timestamp, recipients):
    email = Email(event_id=event_id, subject=subject, content=content, timestamp=timestamp, recipients=recipients) # type: ignore
    email.create()
    return email

@shared_task(ignore_result=False)
def send_email(subject, content, recipients):
    msg = EmailMessage(
        subject,
        content,
        current_app.config['MAIL_DEFAULT_SENDER'],
        [e.strip() for e in recipients.split(';') if e.strip()]
    )
    msg.send()
    return f'Email with subject "{subject}" has been sent to {recipients}.'

@shared_task(ignore_result=False)
def check_scheduled_emails_task():
    """Check if there is any email that needs to be sent."""
    now = datetime.now().replace(second=0, microsecond=0)

    emails = Email.query.filter((Email.timestamp <= now) & (Email.is_sent == False)).all()

    # Sending emails.
    for email in emails:
        send_email.delay(email.subject, email.content, email.recipients) # type: ignore
        email.update(is_sent=True)
    return f'[{now}] - {len(emails)} email(s) were added to the queue for sending.'
