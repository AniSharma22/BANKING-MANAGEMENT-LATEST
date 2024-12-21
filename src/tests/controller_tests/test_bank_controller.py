from unittest.mock import MagicMock

import pytest
from flask import Flask, g

from src.app.controller.bank_urls.bank_routes import BankHandler


class TestBankHandler:

    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture
    def mock_bank_service(self):
        return MagicMock()

    @pytest.fixture
    def bank_handler(self, mock_bank_service):
        return BankHandler.create(mock_bank_service)

    def test_create_bank_success(self, mock_bank_service, bank_handler, app):
        with app.test_request_context(
                json={
                    "bank_name": "test-bank"
                }
        ):
            g.role = "admin"
            _, status_code = bank_handler.create_bank()
            assert status_code == 200
            mock_bank_service.create_new_bank.assert_called_once()

    def test_update_bank_success(self, mock_bank_service, bank_handler, app):
        with app.test_request_context(
                query_string={"new-bank-name": "test-bank-new"},
                json={
                    "bank_name": "test-bank"
                }
        ):
            g.role = "admin"
            _, status_code = bank_handler.update_bank("123")
            assert status_code == 200
            mock_bank_service.update_bank.assert_called_once_with("123", "test-bank-new")

    def test_delete_bank_success(self, mock_bank_service, bank_handler, app):
        with app.test_request_context():
            g.role = "admin"
            _, status_code = bank_handler.delete_bank("123")
            assert status_code == 200
            mock_bank_service.delete_bank.assert_called_once_with("123")

    def test_get_all_banks_success(self, mock_bank_service, bank_handler, app):
        with app.test_request_context():
            _, status_code = bank_handler.get_all_banks()
            assert status_code == 200
            mock_bank_service.get_all_banks.assert_called_once()

    def test_get_user_banks_success(self, mock_bank_service, bank_handler, app):
        with app.test_request_context():
            g.user_id = "123"

            _, status_code = bank_handler.get_user_banks()
            assert status_code == 200
            mock_bank_service.get_user_banks.assert_called_once_with("123")

    def test_get_available_banks_for_user_success(self, mock_bank_service, bank_handler, app):
        with app.test_request_context():
            g.user_id = "123"
            _, status_code = bank_handler.get_available_banks_for_user()
            assert status_code == 200
            mock_bank_service.get_available_banks_for_user.assert_called_once_with("123")
