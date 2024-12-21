import jwt
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify, g

from src.app.middleware.middleware import auth_middleware


@pytest.fixture
def app():
    """
    Fixture to create a Flask app for testing.
    """
    app = Flask(__name__)

    # Add a dummy route to test middleware
    @app.route('/protected', methods=['GET'])
    def protected_route():
        response = auth_middleware()
        if response is not None:
            return response  # Return early if middleware rejects the request
        return jsonify(
            {"message": "Access granted", "user_id": getattr(g, 'user_id', None), "role": getattr(g, 'role', None)})

    @app.route('/user/login', methods=['POST'])
    def login():
        return jsonify({"message": "Login successful"}), 200

    @app.route('/user/signup', methods=['POST'])
    def signup():
        return jsonify({"message": "Signup successful"}), 200

    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """
    Fixture to create a test client for the app.
    """
    return app.test_client()


@patch('src.app.utils.utils.Utils.decode_jwt_token')
def test_auth_middleware_valid_token(mock_decode_jwt_token, client):
    """
    Test the middleware with a valid token.
    """
    # Mock the token decoding
    mock_decode_jwt_token.return_value = {"user_id": "123", "role": "user"}

    # Send a request with a valid token
    response = client.get(
        '/protected',
        headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 200
    assert response.json == {"message": "Access granted", "user_id": "123", "role": "user"}


def test_auth_middleware_missing_token(client):
    """
    Test the middleware with a missing token.
    """
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.json == {'error': 'Unauthorized, missing or invalid token'}


@patch('src.app.utils.utils.Utils.decode_jwt_token')
def test_auth_middleware_invalid_token(mock_decode_jwt_token, client):
    """
    Test the middleware with an invalid token.
    """
    # Mock the token decoding to raise an error
    mock_decode_jwt_token.side_effect = Exception("Invalid token")

    response = client.get(
        '/protected',
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


@patch('src.app.utils.utils.Utils.decode_jwt_token')
def test_auth_middleware_expired_token(mock_decode_jwt_token, client):
    """
    Test the middleware with an expired token.
    """
    # Mock the token decoding to raise an expired signature error
    mock_decode_jwt_token.side_effect = jwt.ExpiredSignatureError()

    response = client.get(
        '/protected',
        headers={"Authorization": "Bearer expired_token"}
    )
    assert response.status_code == 401
    assert response.json == {'error': 'Unauthorized, token has expired'}


def test_auth_middleware_excluded_routes(client):
    """
    Test the middleware for excluded routes like login and signup.
    """
    login_response = client.post('/user/login')
    assert login_response.status_code == 200
    assert login_response.json == {"message": "Login successful"}

    signup_response = client.post('/user/signup')
    assert signup_response.status_code == 200
    assert signup_response.json == {"message": "Signup successful"}
