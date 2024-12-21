from unittest.mock import MagicMock

import pytest
from flask import Flask, g

from src.app.controller.account_controller.account_routes import AccountHandler


class TestAccountHandler:

    @pytest.fixture
    def app(self):
        """Create a Flask app instance for testing"""
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture
    def mock_account_service(self):
        """Create a mock Transaction_service for testing"""
        return MagicMock()

    @pytest.fixture
    def account_handler(self, mock_account_service):
        """Create a UserHandler instance with mock user service"""
        return AccountHandler.create(mock_account_service)

    def test_create_account_success(self, account_handler, mock_account_service, app):
        with app.test_request_context(
                json={
                    "user_id": "1",
                    "branch_id": "12",
                    "bank_id": "123"
                }
        ):
            _, status_code = account_handler.create_account()
            assert status_code == 200
            mock_account_service.create_new_account.assert_called_once()

    def test_get_user_accounts_success(self, account_handler, mock_account_service, app):
        with app.test_request_context():
            g.user_id = "1"
            _, status_code = account_handler.get_user_accounts()
            assert status_code == 200
            mock_account_service.get_user_accounts.assert_called_once()
