from unittest.mock import MagicMock

import pytest

from src.app.models.transaction import Transaction
from src.app.repositories.transaction_repository import TransactionRepository


@pytest.fixture
def mock_db():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_db.get_connection.return_value = mock_conn

    return mock_db, mock_conn, mock_cursor


@pytest.fixture
def transaction_repository(mock_db):
    return TransactionRepository(database=mock_db[0])


# @patch("src.app.repositories.transaction_repository.GenericQueryBuilder")
def test_make_transfer_transaction_success(mock_db, transaction_repository):
    mock_db, mock_conn, mock_cursor = mock_db
    # Mock query results for sender and receiver balances
    mock_cursor.fetchone.side_effect = [
        [2000], [5000]
    ]

    # Create a sample transaction
    transaction = Transaction(
        id="txn123",
        amount=1000,
        transaction_type="transfer",
        sender_acc_id="acc1",
        receiver_acc_id="acc2"
    )

    # Test the method
    transaction_repository.make_transfer_transaction(transaction)
    mock_db.get_connection.return_value.commit.assert_called_once()


def test_make_deposit_transaction_success(mock_db, transaction_repository):
    mock_db, mock_conn, mock_cursor = mock_db
    # Mock query results for sender and receiver balances
    mock_cursor.fetchone.side_effect = [
        [2000]
    ]

    # Create a sample transaction
    transaction = Transaction(
        id="txn123",
        amount=1000,
        transaction_type="transfer",
        sender_acc_id=None,
        receiver_acc_id="acc2"
    )

    transaction_repository.make_deposit_transaction(transaction)
    assert mock_cursor.execute.call_count == 3
    mock_conn.commit.assert_called_once()


def test_make_withdraw_transaction_success(mock_db, transaction_repository):
    mock_db, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.side_effect = [
        [2000]
    ]

    # Create a sample transaction
    transaction = Transaction(
        id="txn123",
        amount=1000,
        transaction_type="transfer",
        sender_acc_id=None,
        receiver_acc_id="acc2"
    )

    transaction_repository.make_withdraw_transaction(transaction)
    assert mock_cursor.execute.call_count == 3
    mock_conn.commit.assert_called_once()


def test_fetch_user_transactions_success(mock_db, transaction_repository):
    # Unpack the mock database, connection, and cursor
    mock_db, mock_conn, mock_cursor = mock_db

    # Create a sample transaction
    transaction = Transaction(
        id="txn123",
        amount=1000,
        transaction_type="transfer",
        sender_acc_id=None,
        receiver_acc_id="acc2",
        time_stamp="2023-12-11T10:00:00"  # Include all fields expected in the Transaction class
    )

    # Mock the cursor's fetchall method to return a list of transaction values
    mock_cursor.fetchall.return_value = [
        [
            transaction.id,
            transaction.amount,
            transaction.transaction_type,
            transaction.sender_acc_id,
            transaction.receiver_acc_id,
            transaction.time_stamp
        ]
    ]

    # Mock the database connection and cursor behavior
    mock_conn.cursor.return_value = mock_cursor
    mock_db.get_connection.return_value = mock_conn

    # Call the method being tested
    transactions = transaction_repository.fetch_user_transactions("123")

    # Assertions to verify correct behavior
    assert len(transactions) == 1
    assert transactions[0].id == transaction.id
    assert transactions[0].amount == transaction.amount
    assert transactions[0].transaction_type == transaction.transaction_type
    assert transactions[0].sender_acc_id == transaction.sender_acc_id
    assert transactions[0].receiver_acc_id == transaction.receiver_acc_id
    assert transactions[0].time_stamp == transaction.time_stamp
