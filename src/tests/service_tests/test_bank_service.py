import pytest
from unittest.mock import MagicMock
from src.app.models.bank import Bank
from src.app.services.bank_service import BankService
from src.app.utils.errors.error import NotExistsError


@pytest.fixture
def mock_bank_repository():
    return MagicMock()


@pytest.fixture
def bank_service(mock_bank_repository):
    return BankService(mock_bank_repository)


def test_get_available_banks_for_user(bank_service, mock_bank_repository):
    mock_banks = [Bank(id="1", name="Bank A"), Bank(id="2", name="Bank B")]
    mock_bank_repository.get_new_banks_for_user.return_value = mock_banks

    result = bank_service.get_available_banks_for_user(user_id="123")

    assert result == mock_banks
    mock_bank_repository.get_new_banks_for_user.assert_called_once_with("123")


def test_get_user_banks(bank_service, mock_bank_repository):
    mock_banks = [Bank(id="3", name="Bank C")]
    mock_bank_repository.fetch_user_banks.return_value = mock_banks

    result = bank_service.get_user_banks(user_id="123")

    assert result == mock_banks
    mock_bank_repository.fetch_user_banks.assert_called_once_with("123")


def test_get_all_banks(bank_service, mock_bank_repository):
    mock_banks = [Bank(id="1", name="Bank A"), Bank(id="2", name="Bank B")]
    mock_bank_repository.get_all_banks.return_value = mock_banks

    result = bank_service.get_all_banks()

    assert result == mock_banks
    mock_bank_repository.get_all_banks.assert_called_once()


def test_create_new_bank(bank_service, mock_bank_repository):
    mock_bank = Bank(id="1", name="New Bank")
    bank_service.create_new_bank(mock_bank)

    mock_bank_repository.create_bank.assert_called_once_with(mock_bank)


def test_update_bank_success(bank_service, mock_bank_repository):
    mock_bank = Bank(id="1", name="Old Bank")
    mock_bank_repository.fetch_bank_by_id.return_value = mock_bank

    bank_service.update_bank(bank_id="1", new_bank_name="Updated Bank")

    mock_bank_repository.update_bank_name.assert_called_once_with("1", "Updated Bank")


def test_update_bank_not_exists(bank_service, mock_bank_repository):
    mock_bank_repository.fetch_bank_by_id.return_value = None

    with pytest.raises(NotExistsError, match="Bank does not exist"):
        bank_service.update_bank(bank_id="1", new_bank_name="Updated Bank")

    mock_bank_repository.update_bank_name.assert_not_called()


def test_delete_bank_success(bank_service, mock_bank_repository):
    mock_bank = Bank(id="1", name="Bank To Delete")
    mock_bank_repository.fetch_bank_by_id.return_value = mock_bank

    bank_service.delete_bank(bank_id="1")

    mock_bank_repository.remove_bank.assert_called_once_with("1")


def test_delete_bank_not_exists(bank_service, mock_bank_repository):
    mock_bank_repository.fetch_bank_by_id.return_value = None

    with pytest.raises(NotExistsError, match="Bank does not exist"):
        bank_service.delete_bank(bank_id="1")

    mock_bank_repository.remove_bank.assert_not_called()


def test_get_bank_by_id(bank_service, mock_bank_repository):
    mock_bank = Bank(id="1", name="Bank A")
    mock_bank_repository.fetch_bank_by_id.return_value = mock_bank

    result = bank_service.get_bank_by_id(bank_id="1")

    assert result == mock_bank
    mock_bank_repository.fetch_bank_by_id.assert_called_once_with("1")
