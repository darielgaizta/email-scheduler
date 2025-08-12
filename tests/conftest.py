import pytest
from app import create_app

@pytest.fixture(scope='session')
def app():
    app = create_app('tests.config.TestConfig')
    app.config.update({
        'CELERY_TASK_ALWAYS_EAGER': True,
        'CELERY_TASK_EAGER_PROPAGATES': True,
    })

    yield app


@pytest.fixture(scope='session')
def celery_app(app):
    celery_app = app.extensions['celery']
    celery_app.conf.update({
        'task_always_eager': True,
        'task_eager_propagates': True,
    })
    return celery_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()