import pytest
from unittest.mock import MagicMock
from src.app.models.user import User
from src.app.repositories.user_repository import UserRepository
from src.app.utils.errors.error import DatabaseError


@pytest.fixture
def mock_db():
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db = MagicMock()

    # Simulate the connection returning the mocked cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_db.get_connection.return_value = mock_conn

    return mock_db, mock_conn, mock_cursor


@pytest.fixture
def user_repository(mock_db):
    # Initialize the repository with the mocked database
    return UserRepository(database=mock_db[0])


def test_save_user(mock_db, user_repository):
    mock_conn, mock_cursor = mock_db[1], mock_db[2]

    # Mock user object
    user = User(
        id="1",
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword",
        phone_no="1234567890",
        address="123 Main St",
        role="user"
    )

    # Call the method
    user_repository.save_user(user)

    # Assertions
    mock_conn.execute.assert_called_once()
    query, values = mock_conn.execute.call_args[0]
    assert "INSERT INTO users" in query
    assert values == [val for val in user.__dict__.values()]


def test_fetch_user_by_email(mock_db, user_repository):
    mock_conn, mock_cursor = mock_db[1], mock_db[2]

    # Define mock result from database
    mock_cursor.fetchone.return_value = (
        "1", "John Doe", "john.doe@example.com", "securepassword",
        "1234567890", "123 Main St", "user"
    )

    # Call the method
    user = user_repository.fetch_user_by_email("john.doe@example.com")

    # Assertions
    mock_cursor.execute.assert_called_once()
    query, values = mock_cursor.execute.call_args[0]
    assert "SELECT" in query  # Check query type
    assert values == ["john.doe@example.com"]  # Ensure email is passed
    assert user is not None  # Ensure a user is returned
    assert user.name == "John Doe"  # Validate returned data


def test_fetch_user_by_email_not_found(mock_db, user_repository):
    mock_conn, mock_cursor = mock_db[1], mock_db[2]

    # Simulate no results from database
    mock_cursor.fetchone.return_value = None

    # Call the method
    user = user_repository.fetch_user_by_email("nonexistent@example.com")

    # Assertions
    assert user is None  # Ensure None is returned


def test_save_user_raises_error(mock_db, user_repository):
    mock_conn, _ = mock_db[1], mock_db[2]

    # Simulate an exception
    mock_conn.execute.side_effect = Exception("Database Error")

    # Mock user object
    user = User(
        id="1",
        name="John Doe",
        email="john.doe@example.com",
        password="securepassword",
        phone_no="1234567890",
        address="123 Main St",
        role="user"
    )

    # Test for exception
    with pytest.raises(DatabaseError):
        user_repository.save_user(user)


def test_fetch_user_by_email_raises_error(mock_db, user_repository):
    _, mock_cursor = mock_db[1], mock_db[2]

    # Simulate an exception
    mock_cursor.execute.side_effect = Exception("Database Error")

    # Test for exception
    with pytest.raises(DatabaseError):
        user_repository.fetch_user_by_email("testemail@gmail.com")
