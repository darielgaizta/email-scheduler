from celery import Celery
from flask import Flask
from celery.schedules import crontab

from .extensions import db, mail, migrate
from .routes import email

import logging


def celery_init_app(app: Flask) -> Celery:
    celery_app = Celery(app.name)
    celery_app.config_from_object(app.config['CELERY'])
    celery_app.set_default()

    TaskBase = celery_app.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery_app.Task = ContextTask
    
    app.extensions['celery'] = celery_app
    return celery_app


def create_app(config='config.Config'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis:6379/0",
            result_backend="redis://redis:6379/0",
            task_ignore_result=True,
            beat_schedule={
                "check-emails-every-minute": {
                    "task": "app.services.email.check_scheduled_emails_task",
                    "schedule": crontab(minute="*") # Every minute
                }
            }
        ),
    )
    celery_init_app(app)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # Initialize extensions.
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Blueprint registration.
    app.register_blueprint(email.bp)

    return app