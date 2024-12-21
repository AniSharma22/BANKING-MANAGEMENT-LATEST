import pytest
from unittest.mock import MagicMock
from src.app.services.transaction_service import TransactionService
from src.app.models.transaction import Transaction
from src.app.utils.types import TransactionType
from src.app.utils.errors.error import InvalidOperationError, NotExistsError
from src.app.models.account import Account  # Assuming Account is defined


@pytest.fixture
def mock_transaction_repository():
    return MagicMock()


@pytest.fixture
def mock_account_service():
    return MagicMock()


@pytest.fixture
def transaction_service(mock_transaction_repository, mock_account_service):
    return TransactionService(mock_transaction_repository, mock_account_service)


@pytest.fixture
def sample_transaction():
    return Transaction(
        transaction_type=TransactionType.DEPOSIT.value,
        sender_acc_id="123",
        receiver_acc_id="456",
        amount=100
    )


@pytest.fixture
def sample_account():
    return Account(
        id="123",
        user_id="user_1",
        branch_id="branch-1",
        bank_id="bank-1",
        balance=500
    )


def test_create_transaction_deposit(transaction_service, sample_transaction, mock_account_service):
    sample_transaction.transaction_type = TransactionType.DEPOSIT.value
    mock_account_service.get_account_by_id.return_value = MagicMock(user_id="user_1")

    transaction_service.create_transaction(sample_transaction, user_id="user_1")

    transaction_service.transaction_repository.make_deposit_transaction.assert_called_once_with(sample_transaction)


def test_create_transaction_withdrawal(transaction_service, sample_transaction, mock_account_service):
    sample_transaction.transaction_type = TransactionType.WITHDRAW.value
    mock_account_service.get_account_by_id.return_value = MagicMock(user_id="user_1")

    transaction_service.create_transaction(sample_transaction, user_id="user_1")

    transaction_service.transaction_repository.make_withdraw_transaction.assert_called_once_with(sample_transaction)


def test_create_transaction_transfer(transaction_service, sample_transaction, mock_account_service):
    sample_transaction.transaction_type = TransactionType.TRANSFER.value
    mock_account_service.get_account_by_id.side_effect = [
        MagicMock(user_id="user_1"),  # Sender account
        MagicMock(user_id="user_2")  # Receiver account
    ]

    transaction_service.create_transaction(sample_transaction, user_id="user_1")

    transaction_service.transaction_repository.make_transfer_transaction.assert_called_once_with(sample_transaction)


def test_create_transaction_invalid_type(transaction_service, sample_transaction):
    sample_transaction.transaction_type = "INVALID"

    with pytest.raises(InvalidOperationError):
        transaction_service.create_transaction(sample_transaction, user_id="user_1")


def test_initiate_withdrawal_invalid_account(transaction_service, sample_transaction, mock_account_service):
    sample_transaction.transaction_type = TransactionType.WITHDRAW.value
    mock_account_service.get_account_by_id.return_value = None

    with pytest.raises(NotExistsError):
        transaction_service._initiate_withdrawal(sample_transaction, user_id="user_1")


def test_initiate_transfer_same_account(transaction_service, sample_transaction):
    sample_transaction.sender_acc_id = "123"
    sample_transaction.receiver_acc_id = "123"

    with pytest.raises(InvalidOperationError):
        transaction_service._initiate_transfer(sample_transaction, user_id="user_1")


def test_view_transactions_unauthorized(transaction_service, mock_account_service):
    mock_account_service.get_account_by_id.return_value = MagicMock(user_id="user_2")  # Not the user

    with pytest.raises(PermissionError):
        transaction_service.view_transactions(user_id="user_1", account_id="123")


def test_view_transactions_success(transaction_service, mock_transaction_repository, mock_account_service):
    mock_account_service.get_account_by_id.return_value = MagicMock(user_id="user_1")
    mock_transaction_repository.fetch_user_transactions.return_value = ["txn1", "txn2"]

    transactions = transaction_service.view_transactions(user_id="user_1", account_id="123")

    assert transactions == ["txn1", "txn2"]
