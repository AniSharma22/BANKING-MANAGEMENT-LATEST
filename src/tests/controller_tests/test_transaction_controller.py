from unittest import TestCase
from unittest.mock import MagicMock

import pytest
from flask import Flask, g

from src.app.controller.transaction_controller.transaction_routes import TransactionHandler
from src.app.models.transaction import Transaction


class TestTransactionHandler(TestCase):

    @pytest.fixture
    def app(self):
        """Create a Flask app instance for testing"""
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture
    def mock_transaction_service(self):
        """Create a mock Transaction_service for testing    """
        return MagicMock()

    @pytest.fixture
    def transaction_handler(self, mock_transaction_service):
        """Create a UserHandler instance with mock user service"""
        return TransactionHandler.create(mock_transaction_service)

    def test_create_transfer_transaction_success(self, transaction_handler, mock_transaction_service, app):
        with app.test_request_context(
                query_string={
                    "transaction_type": "transfer"
                },
                json={
                    "sender_acc_id": "12345",
                    "receiver_acc_id": "23456",
                    "amount": 200
                }
        ):
            g.user_id = "123"

            result, status_code = transaction_handler.create_transaction()
            assert status_code == 201
            mock_transaction_service.create_transaction.assert_called_once()

    def test_view_transaction_success(self, transaction_handler, mock_transaction_service, app):
        mock_transaction_service.view_transactions.return_value = [Transaction(100, "transfer"),
                                                                   Transaction(200, "withdraw")]

        with app.test_request_context(
                query_string={
                    "account_id": "12345",
                }
        ):
            g.user_id = "123"

            result, status_code = transaction_handler.view_transaction()
            assert status_code == 200
            mock_transaction_service.view_transactions.assert_called_once_with("123","12345")

