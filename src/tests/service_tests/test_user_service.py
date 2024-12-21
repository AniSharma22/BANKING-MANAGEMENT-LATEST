from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.app.models.user import User
from src.app.repositories.user_repository import UserRepository
from src.app.services.user_service import UserService
from src.app.utils.errors.error import UserExistsError, InvalidCredentialsError


class TestUserService(TestCase):
    mock_user = User(email="test@example.com", password="password123", name="test", phone_no="test123", address="Test")

    def setUp(self):
        self.mock_user_repository = MagicMock(spec=UserRepository)
        self.user_service = UserService(self.mock_user_repository)

    def test_signup_user_success(self):
        # Mock repository behavior
        self.mock_user_repository.fetch_user_by_email.return_value = None
        self.mock_user_repository.save_user.return_value = None

        result = self.user_service.signup_user(self.mock_user)

        # Assertions
        self.mock_user_repository.fetch_user_by_email.assert_called_once_with("test@example.com")
        self.mock_user_repository.save_user.assert_called_once_with(self.mock_user)

    def test_signup_user_already_exists(self):
        # Mock repository behavior
        self.mock_user_repository.fetch_user_by_email.return_value = self.mock_user

        with self.assertRaises(UserExistsError):
            self.user_service.signup_user(self.mock_user)

    def test_login_user_success(self):
        self.mock_user_repository.fetch_user_by_email.return_value = self.mock_user
        with patch('src.app.utils.utils.Utils.check_password', return_value=True) as mock_check_password:
            result = self.user_service.login_user("test-email", "test-password")

            self.mock_user_repository.fetch_user_by_email.assert_called_once_with("test-email")
            mock_check_password.assert_called_once()
            self.assertEqual(result, self.mock_user)

    def test_login_user_invalid_credentials(self):
        # Mock repository behavior
        self.mock_user_repository.fetch_user_by_email.return_value = None

        with self.assertRaises(InvalidCredentialsError):
            self.user_service.login_user("test@example.com", "wrongpassword")

        # Mock repository returns a user but password check fails
        self.mock_user_repository.fetch_user_by_email.return_value = self.mock_user

        with patch('src.app.utils.utils.Utils.check_password', return_value=False):
            with self.assertRaises(InvalidCredentialsError):
                self.user_service.login_user("test@example.com", "wrongpassword")
