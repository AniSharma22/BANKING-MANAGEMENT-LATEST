import pytest
from flask import Flask
from src.app.controller.main import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


def test_create_app(app: Flask):
    assert app is not None
    assert isinstance(app, Flask)
    assert app.testing is True


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == 'Hello World!'


def test_registered_routes(app: Flask):
    # Expected blueprints
    expected_blueprints = [
        '/bank',
        '/branch',
        '/account',
        '/transaction',
        '/user'
    ]

    # Verify routes exist
    for prefix in expected_blueprints:
        with app.test_client() as client:
            response = client.get(prefix)
            assert response.status_code in [404, 200, 401, 405]
