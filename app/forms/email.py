from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import InputRequired, ValidationError, NumberRange, Length

import re

def validate_recipients(form, field):
    email_pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9._%+-]*[a-zA-Z0-9])?@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    recipients = [e.strip() for e in field.data.split(';') if e.strip()]
    for recipient in recipients:
        if re.search(r'\s', recipient) or not re.match(email_pattern, recipient):
            raise ValidationError(f"Invalid email address: {recipient}")

class SendEmailForm(FlaskForm):
    event_id = IntegerField('Event ID', [InputRequired(), NumberRange(min=1, message="Event ID must be greater than 0.")])
    subject = StringField('Subject', [InputRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', [InputRequired()])
    timestamp = DateTimeField('Timestamp', [InputRequired()], format='%d %b %Y %H:%M')
    recipients = StringField('Recipients (separated by semicolon)', [InputRequired(), validate_recipients])