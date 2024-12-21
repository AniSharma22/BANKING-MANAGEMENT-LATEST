from unittest.mock import MagicMock

import pytest

from src.app.models.bank import Bank
from src.app.repositories.bank_repository import BankRepository
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
def bank_repository(mock_db):
    return BankRepository(database=mock_db[0])


def test_create_bank(bank_repository, mock_db):
    mock_db, mock_conn, mock_cursor = mock_db[0], mock_db[1], mock_db[2]

    test_bank = Bank(id="bank_123", name="Test Bank")

    bank_repository.create_bank(test_bank)

    query, values = mock_conn.execute.call_args[0]
    mock_db.get_connection.assert_called_once()
    mock_conn.execute.assert_called_once()
    assert "INSERT INTO banks" in query
    assert [test_bank.id, test_bank.name] == values


def test_create_bank_database_error(bank_repository, mock_db):
    mock_db, mock_conn, _ = mock_db[0], mock_db[1], mock_db[2]

    mock_conn.execute.side_effect = DatabaseError("DB error")
    test_bank = Bank(id="bank_123", name="Test Bank")

    with pytest.raises(DatabaseError, match="DB error"):
        bank_repository.create_bank(test_bank)


def test_get_all_banks(bank_repository, mock_db):
    mock_db, mock_conn, mock_cursor = mock_db[0], mock_db[1], mock_db[2]

    mock_cursor.fetchall.return_value = [("bank_123", "Bank 1"), ("bank_456", "Bank 2")]

    banks = bank_repository.get_all_banks()

    mock_db.get_connection.assert_called_once()
    mock_cursor.execute.assert_called_once_with(('SELECT id, name FROM banks', []))
    assert len(banks) == 2
    assert banks[0].id == "bank_123"
    assert banks[0].name == "Bank 1"


def test_get_new_banks_for_user(bank_repository, mock_db):
    mock_db, mock_conn, mock_cursor = mock_db[0], mock_db[1], mock_db[2]

    mock_cursor.fetchall.return_value = [("bank_789", "Bank 3")]

    banks = bank_repository.get_new_banks_for_user(user_id="user_123")

    mock_db.get_connection.assert_called_once()
    mock_cursor.execute.assert_called_once()
    assert len(banks) == 1
    assert banks[0].id == "bank_789"
    assert banks[0].name == "Bank 3"


def test_update_bank_name(bank_repository, mock_db):
    mock_db, mock_conn, _ = mock_db[0], mock_db[1], mock_db[2]

    bank_repository.update_bank_name(bank_id="bank_123", new_bank_name="Updated Bank Name")

    query, values = mock_conn.cursor.return_value.execute.call_args[0]
    assert "UPDATE banks SET name = ?" in query


def test_remove_bank(bank_repository, mock_db):
    mock_db, mock_conn, _ = mock_db[0], mock_db[1], mock_db[2]

    bank_repository.remove_bank(bank_id="bank_123")

    query, values = mock_conn.cursor.return_value.execute.call_args[0]
    assert "DELETE FROM banks WHERE id = ?" in query


def test_fetch_user_banks(bank_repository, mock_db):
    mock_db, mock_conn, mock_cursor = mock_db[0], mock_db[1], mock_db[2]

    mock_cursor.fetchall.return_value = [("bank_123", "User Bank 1")]

    banks = bank_repository.fetch_user_banks(user_id="user_123")

    mock_db.get_connection.assert_called_once()
    mock_cursor.execute.assert_called_once()
    assert len(banks) == 1
    assert banks[0].id == "bank_123"
    assert banks[0].name == "User Bank 1"


def test_fetch_bank_by_id(bank_repository, mock_db):
    mock_db, mock_conn, mock_cursor = mock_db[0], mock_db[1], mock_db[2]

    mock_cursor.fetchone.return_value = ("bank_123", "Fetched Bank")

    bank = bank_repository.fetch_bank_by_id(bank_id="bank_123")

    mock_db.get_connection.assert_called_once()
    mock_cursor.execute.assert_called_once()
    assert bank.id == "bank_123"
    assert bank.name == "Fetched Bank"
