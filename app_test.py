import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_exists(app):
    assert app is not None

def test_db_exists(app):
    assert db is not None


def test_login_required(client):
    response = client.get('/deposit')  # Assuming /dashboard requires login
    assert response.status_code == 302
    assert '/' in response.headers['Location']

from . models import User

def test_user_loader(app):
    with app.app_context():
        user = User(uid=1, username='testuser', password='testpass')
        db.session.add(user)
        db.session.commit()
        loaded_user = User.query.get(1)
        assert loaded_user is not None
        assert loaded_user.username == 'testuser'

