from unittest.mock import MagicMock, patch

import pytest

from src.app.models.account import Account
from src.app.services.account_service import AccountService


@pytest.fixture
def mock_account_repository():
    return MagicMock()


@pytest.fixture
def mock_branch_service():
    return MagicMock()


@pytest.fixture
def account_service(mock_account_repository, mock_branch_service):
    return AccountService(mock_account_repository, mock_branch_service)


def test_create_new_account_success(account_service, mock_account_repository, mock_branch_service):
    test_account = Account(user_id="user-1", branch_id="branch-1", bank_id="bank-1")
    mock_branch_service.get_branch_by_id.return_value = test_account
    mock_account_repository.user_account_exists.return_value = False

    account_service.create_new_account(test_account)

    mock_account_repository.create_account.assert_called_once_with(test_account)
    mock_branch_service.get_branch_by_id.assert_called_once_with(test_account.branch_id)
    mock_account_repository.user_account_exists.assert_called_once_with(test_account.user_id, test_account.bank_id)


def test_get_account_by_id(account_service, mock_account_repository):
    test_account = Account(user_id="user-1", branch_id="branch-1", bank_id="bank-1")
    mock_account_repository.fetch_account_by_id.return_value = test_account

    result = account_service.get_account_by_id(test_account.user_id)

    mock_account_repository.fetch_account_by_id.assert_called_once_with(test_account.user_id)
    assert result == test_account


@patch("src.app.services.account_service.AccountService.get_account_by_id")
def test_delete_account(mock_get_account_by_id, account_service, mock_account_repository):
    test_account = Account(user_id="user-1", branch_id="branch-1", bank_id="bank-1")
    mock_get_account_by_id.return_value = test_account

    account_service.delete_account(test_account.user_id, test_account.id)

    mock_account_repository.delete_account.assert_called_once_with(test_account)


def test_get_user_accounts(account_service, mock_account_repository):
    test_account = Account(user_id="user-1", branch_id="branch-1", bank_id="bank-1")
    mock_account_repository.fetch_all_user_accounts.return_value = [test_account]

    account_service.get_user_accounts(test_account.user_id)

    mock_account_repository.fetch_all_user_accounts.assert_called_once_with(test_account.user_id)
