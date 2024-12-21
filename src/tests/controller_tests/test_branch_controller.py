from unittest.mock import MagicMock

import pytest
from flask import Flask, g

from src.app.controller.branch_controller.branch_routes import BranchHandler


class TestBranchHandler:

    @pytest.fixture
    def app(self):
        """Create a Flask app instance for testing"""
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    @pytest.fixture
    def mock_branch_service(self):
        """Create a mock Transaction_service for testing"""
        return MagicMock()

    @pytest.fixture
    def branch_handler(self, mock_branch_service):
        """Create a UserHandler instance with mock user service"""
        return BranchHandler.create(mock_branch_service)

    def test_create_branch_success(self, mock_branch_service, branch_handler, app):
        with app.test_request_context(
                json={
                    "branch_name": "hdfc_3",
                    "branch_address": "jaipur",
                    "bank_id": "123"
                }
        ):
            g.role = "admin"
            result, status_code = branch_handler.create_branch()
            assert status_code == 200
            mock_branch_service.create_new_branch.assert_called_once()

    def test_update_branch_success(self, mock_branch_service, branch_handler, app):
        with app.test_request_context(
                json={
                    "new_branch_name": "hdfc_3",
                    "new_branch_address": "jaipur",
                }
        ):
            g.role = "admin"
            result, status_code = branch_handler.update_branch("1234")
            assert status_code == 200
            mock_branch_service.update_branch_details.assert_called_once_with("1234", "hdfc_3", "jaipur")

    def test_delete_branch_success(self, mock_branch_service, branch_handler, app):
        with app.test_request_context():
            g.role = "admin"
            result, status_code = branch_handler.delete_branch("1234")
            assert status_code == 200
            mock_branch_service.remove_branch.assert_called_once_with("1234")

    def test_admin_permission_error(self, mock_branch_service, branch_handler, app):
        with app.test_request_context():
            g.role = "user"
            result, status_code = branch_handler.delete_branch("1234")
            assert status_code == 403

    def test_get_bank_branches_success(self, mock_branch_service, branch_handler, app):
        with app.test_request_context():
            result, status_code = branch_handler.get_bank_branches("123")

            mock_branch_service.get_bank_branches.assert_called_once_with("123")
            assert status_code == 200
