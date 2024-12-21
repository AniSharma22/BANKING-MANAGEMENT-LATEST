import pytest
from unittest.mock import MagicMock
from src.app.models.branch import Branch
from src.app.services.branch_service import BranchService
from src.app.utils.errors.error import NotExistsError


@pytest.fixture
def mock_branch_repository():
    return MagicMock()


@pytest.fixture
def mock_bank_service():
    return MagicMock()


@pytest.fixture
def branch_service(mock_branch_repository, mock_bank_service):
    return BranchService(mock_branch_repository, mock_bank_service)


def test_get_bank_branches_success(branch_service, mock_branch_repository, mock_bank_service):
    mock_bank_service.get_bank_by_id.return_value = True
    mock_branches = [
        Branch(id="1", name="Branch A", address="Address A", bank_id="123"),
        Branch(id="2", name="Branch B", address="Address B", bank_id="123"),
    ]
    mock_branch_repository.fetch_bank_branches.return_value = mock_branches

    result = branch_service.get_bank_branches(bank_id="123")

    assert result == mock_branches
    mock_bank_service.get_bank_by_id.assert_called_once_with("123")
    mock_branch_repository.fetch_bank_branches.assert_called_once_with("123")


def test_get_bank_branches_bank_not_exists(branch_service, mock_bank_service):
    mock_bank_service.get_bank_by_id.return_value = None

    with pytest.raises(NotExistsError, match="Bank does not exist"):
        branch_service.get_bank_branches(bank_id="123")

    mock_bank_service.get_bank_by_id.assert_called_once_with("123")


def test_create_new_branch(branch_service, mock_branch_repository):
    mock_branch = Branch(id="1", name="New Branch", address="Address", bank_id="123")

    branch_service.create_new_branch(mock_branch)

    mock_branch_repository.create_branch.assert_called_once_with(mock_branch)


def test_update_branch_details_success(branch_service, mock_branch_repository):
    mock_branch = Branch(id="1", name="Old Branch", address="Old Address", bank_id="123")
    mock_branch_repository.fetch_branch_by_id.return_value = mock_branch

    branch_service.update_branch_details(branch_id="1", new_branch_name="Updated Branch",
                                         new_branch_address="New Address")

    mock_branch_repository.update_branch.assert_called_once_with("1", "Updated Branch", "New Address")


def test_update_branch_details_partial_update(branch_service, mock_branch_repository):
    mock_branch = Branch(id="1", name="Old Branch", address="Old Address", bank_id="123")
    mock_branch_repository.fetch_branch_by_id.return_value = mock_branch

    branch_service.update_branch_details(branch_id="1", new_branch_name=None, new_branch_address="New Address")

    mock_branch_repository.update_branch.assert_called_once_with("1", "Old Branch", "New Address")


def test_update_branch_details_not_exists(branch_service, mock_branch_repository):
    mock_branch_repository.fetch_branch_by_id.return_value = None

    with pytest.raises(NotExistsError, match="Branch does not exist"):
        branch_service.update_branch_details(branch_id="1", new_branch_name="Updated Branch",
                                             new_branch_address="New Address")

    mock_branch_repository.update_branch.assert_not_called()


def test_remove_branch_success(branch_service, mock_branch_repository):
    mock_branch = Branch(id="1", name="Branch A", address="Address A", bank_id="123")
    mock_branch_repository.fetch_branch_by_id.return_value = mock_branch

    branch_service.remove_branch(branch_id="1")

    mock_branch_repository.delete_branch.assert_called_once_with("1")


def test_remove_branch_not_exists(branch_service, mock_branch_repository):
    mock_branch_repository.fetch_branch_by_id.return_value = None

    with pytest.raises(NotExistsError, match="Branch does not exist"):
        branch_service.remove_branch(branch_id="1")

    mock_branch_repository.delete_branch.assert_not_called()


def test_get_branch_by_id(branch_service, mock_branch_repository):
    mock_branch = Branch(id="1", name="Branch A", address="Address A", bank_id="123")
    mock_branch_repository.fetch_branch_by_id.return_value = mock_branch

    result = branch_service.get_branch_by_id(branch_id="1")

    assert result == mock_branch
    mock_branch_repository.fetch_branch_by_id.assert_called_once_with("1")
