from unittest.mock import MagicMock
import pytest

from src.app.models.account import Account
from src.app.repositories.account_repository import AccountRepository
from src.app.utils.errors.error import DatabaseError


@pytest.fixture
def mock_db():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_db.get_connection.return_value = mock_conn

    return mock_db, mock_conn, mock_cursor


@pytest.fixture
def account_repository(mock_db):
    return AccountRepository(database=mock_db[0])


def test_create_account_success(mock_db, account_repository):
    _, mock_conn, _ = mock_db
    account = Account(id="1", user_id="user123", branch_id="branch456", bank_id="bank789", balance=1000)

    account_repository.create_account(account)

    mock_conn.execute.assert_called_once()


def test_delete_account_success(mock_db, account_repository):
    _, mock_conn, _ = mock_db

    account_repository.delete_account("account123")

    mock_conn.execute.assert_called_once()


def test_fetch_account_by_id_success(mock_db, account_repository):
    _, _, mock_cursor = mock_db

    mock_cursor.fetchone.return_value = ("1", "user123", "branch456", "bank789", 1000)

    account = account_repository.fetch_account_by_id("account123")

    assert account == Account(id="1", user_id="user123", branch_id="branch456", bank_id="bank789", balance=1000)


def test_fetch_account_by_id_not_found(mock_db, account_repository):
    _, _, mock_cursor = mock_db

    mock_cursor.fetchone.return_value = None

    account = account_repository.fetch_account_by_id("nonexistent")

    assert account is None


def test_fetch_all_user_accounts_success(mock_db, account_repository):
    _, _, mock_cursor = mock_db

    mock_cursor.fetchall.return_value = [
        ("1", "user123", "branch456", "bank789", 1000),
        ("2", "user123", "branch789", "bank789", 500),
    ]

    accounts = account_repository.fetch_all_user_accounts("user123")

    assert len(accounts) == 2
    assert accounts[0] == Account(id="1", user_id="user123", branch_id="branch456", bank_id="bank789", balance=1000)
    assert accounts[1] == Account(id="2", user_id="user123", branch_id="branch789", bank_id="bank789", balance=500)


def test_fetch_all_user_accounts_empty(mock_db, account_repository):
    _, _, mock_cursor = mock_db

    mock_cursor.fetchall.return_value = []

    accounts = account_repository.fetch_all_user_accounts("nonexistent")

    assert accounts == []


def test_user_account_exists_true(mock_db, account_repository):
    _, _, mock_cursor = mock_db

    mock_cursor.fetchone.return_value = ("1",)

    exists = account_repository.user_account_exists("user123", "bank789")

    assert exists is True


def test_user_account_exists_false(mock_db, account_repository):
    _, _, mock_cursor = mock_db

    mock_cursor.fetchone.return_value = None

    exists = account_repository.user_account_exists("user123", "nonexistent")

    assert exists is False


def test_create_account_raises_exception(mock_db, account_repository):
    _, mock_conn, _ = mock_db
    mock_conn.execute.side_effect = Exception("Database error")
    account = Account(id="1", user_id="user123", branch_id="branch456", bank_id="bank789", balance=1000)

    with pytest.raises(DatabaseError, match="Database error"):
        account_repository.create_account(account)


def test_delete_account_raises_exception(mock_db, account_repository):
    _, mock_conn, _ = mock_db
    mock_conn.execute.side_effect = Exception("Database error")

    with pytest.raises(DatabaseError, match="Database error"):
        account_repository.delete_account("account123")
