import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask

from src.app.controller.user_controller.user_routes import UserHandler


class TestUserHandler:
    @pytest.fixture
    def app(self):
        """Create a Flask app instance f or testing"""
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture
    def mock_user_service(self):
        """Create a mock UserService for testing"""
        return MagicMock()

    @pytest.fixture
    def user_handler(self, mock_user_service):
        """Create a UserHandler instance with mock user service"""
        return UserHandler.create(mock_user_service)

    @patch('src.app.utils.utils.Utils.create_jwt_token')
    def test_login_successful(self, mock_create_token, app, user_handler, mock_user_service):
        """Test successful login"""
        # Prepare mock data
        mock_user = Mock(
            id='user123',
            role='customer'
        )
        # Configure mock service to return a user
        mock_user_service.login_user.return_value = mock_user

        # Set return value for mocked token creation
        mock_token = "dummy.jwt.token"
        mock_create_token.return_value = mock_token

        # Simulate request context with the correct Content-Type
        with app.test_request_context(
                json={
                    'email': 'test@gmail.com',
                    'password': 'validpassword'
                },
        ):
            # Call login method
            response, status_code = user_handler.login()

            # Assertions
            assert status_code == 200
            assert response.json["token"] == mock_token
            assert response.json["role"] == mock_user.role

            # Verify service was called correctly
            mock_user_service.login_user.assert_called_once_with(
                'test@gmail.com',
                'validpassword'
            )

    @patch('src.app.utils.utils.Utils.create_jwt_token')
    def test_signup_successful(self, mock_create_token, app, user_handler, mock_user_service):
        with app.test_request_context(
                json={
                    "name": "Anish",
                    "email": "test@gmail.com",
                    "password": "Test2003@",
                    "phone_no": "8888888888",
                    "address": "supertech"
                }
        ):
            mock_create_token.return_value = "token"

            result, status_code = user_handler.signup()

            mock_user_service.signup_user.assert_called_once()
            assert status_code == 200

    def test_create_success(self, user_handler, mock_user_service):
        test_user_handler = user_handler.create(mock_user_service)
        assert isinstance(test_user_handler, UserHandler)
