import pytest

from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_users(app, client):
    res = client.get('/users')
    assert res.status_code == 200


def test_admin_user(app, client):
    res = client.get('/users/yw3936@columbia.edu')
    assert res.status_code == 200