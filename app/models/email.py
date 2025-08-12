from app.extensions import db
from . import Mixin

class Email(Mixin, db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False, unique=True)
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    recipients = db.Column(db.Text, nullable=False)
    is_sent = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Email(id={self.id}, subject='{self.subject}', recipient='{self.recipients}')>, is_sent={self.is_sent})"