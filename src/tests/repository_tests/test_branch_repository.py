from unittest.mock import MagicMock
import pytest

from src.app.repositories.branch_repository import BranchRepository
from src.app.models.branch import Branch
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
def branch_repository(mock_db):
    return BranchRepository(database=mock_db[0])


def test_fetch_bank_branches_success(mock_db, branch_repository):
    _, mock_conn, mock_cursor = mock_db

    mock_cursor.fetchall.return_value = [
        ("1", "123", "Branch A", "Address A"),
        ("2", "123", "Branch B", "Address B"),
    ]

    branches = branch_repository.fetch_bank_branches("123")

    assert len(branches) == 2
    assert branches[0] == Branch(id="1", bank_id="123", name="Branch A", address="Address A")
    assert branches[1] == Branch(id="2", bank_id="123", name="Branch B", address="Address B")


def test_fetch_bank_branches_empty(mock_db, branch_repository):
    _, mock_conn, mock_cursor = mock_db

    mock_cursor.fetchall.return_value = None

    branches = branch_repository.fetch_bank_branches("123")

    mock_cursor.execute.assert_called_once()

    assert branches is None


def test_create_branch_success(mock_db, branch_repository):
    branch = Branch(id="1", bank_id="123", name="Branch A", address="Address A")

    branch_repository.create_branch(branch)

    mock_db[0].get_connection().execute.assert_called_once()


def test_create_branch_error(mock_db, branch_repository):
    branch = Branch(id="1", bank_id="123", name="Branch A", address="Address A")

    mock_db[0].get_connection().execute.side_effect = Exception("DB Error")

    with pytest.raises(DatabaseError, match="DB Error"):
        branch_repository.create_branch(branch)


def test_update_branch_success(mock_db, branch_repository):
    branch_id = "1"
    new_name = "Updated Branch"
    new_address = "Updated Address"

    branch_repository.update_branch(branch_id, new_name, new_address)

    mock_db[0].get_connection().execute.assert_called_once()


def test_delete_branch_success(mock_db, branch_repository):
    branch_id = "1"

    branch_repository.delete_branch(branch_id)

    mock_db[0].get_connection().execute.assert_called_once()


def test_fetch_branch_by_id_success(mock_db, branch_repository):
    _, mock_conn, mock_cursor = mock_db

    mock_cursor.fetchone.return_value = ("1", "123", "Branch A", "Address A")

    branch = branch_repository.fetch_branch_by_id("1")

    mock_cursor.execute.assert_called_once()

    assert branch == Branch(id="1", bank_id="123", name="Branch A", address="Address A")


def test_fetch_branch_by_id_not_found(mock_db, branch_repository):
    _, mock_conn, mock_cursor = mock_db

    mock_cursor.fetchone.return_value = None

    branch = branch_repository.fetch_branch_by_id("1")

    mock_cursor.execute.assert_called_once()

    assert branch is None
