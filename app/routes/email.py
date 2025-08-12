from flask import Blueprint, render_template, request
from app.forms.email import SendEmailForm
from app.services.email import save_email

from datetime import datetime

bp = Blueprint('email', __name__)

@bp.route('/save_emails', methods=('GET', 'POST'))
def save_emails():
    form = SendEmailForm(request.form)

    if request.method == 'POST' and form.validate():
        event_id = form.event_id.data
        email_subject = form.subject.data
        email_content = form.content.data
        recipients = form.recipients.data

        try:
            utc_timestamp = request.form.get('utc_timestamp')
            if not utc_timestamp:
                return "UTC timestamp is required", 400
            timestamp = datetime.fromisoformat(utc_timestamp.replace('Z', '+00:00'))
        except Exception as e:
            return f"Error parsing UTC timestamp: {e}", 400
        
        # Save to database
        save_email(event_id, email_subject, email_content, timestamp, recipients)
        return f'Email has been saved and will be sent at {timestamp} (Server-time), thank you for using this application!'

    return render_template('save_emails.html', form=form)