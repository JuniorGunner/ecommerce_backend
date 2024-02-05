from unittest.mock import MagicMock
from datetime import timedelta
import pytest
from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserSchema
from services import user_service
from jose import jwt

# User data for testing
user_data = UserSchema(
    username="testuser", email="test@example.com", password="testpassword"
)


# Mocking the database session for all tests
@pytest.fixture
def mock_db_session(mocker):
    # Mock the SessionLocal class to return a mock session
    mock_session = mocker.MagicMock(spec=Session)
    mocker.patch("database.SessionLocal", return_value=mock_session)
    return mock_session


def test_create_user(mock_db_session):
    # Mock the UserModel.query to prevent actual DB calls
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    # Call the service function with the mocked session
    user = user_service.create_user(mock_db_session, user_data)

    # Assertions to ensure the service function behaves as expected
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_verify_password():
    password = "secret"
    hashed_password = user_service.get_password_hash(password)
    assert user_service.verify_password(password, hashed_password) is True


def test_authenticate_user(mocker, mock_db_session):
    # Mock get_user to return a mock user
    mock_user = UserModel(
        username=user_data.username, hashed_password="hashed_password"
    )
    mocker.patch("services.user_service.get_user", return_value=mock_user)

    # Mock verify_password to return True
    mocker.patch("services.user_service.verify_password", return_value=True)

    # Call the service function
    user = user_service.authenticate_user(mock_db_session, user_data.username, user_data.password)

    # Assertions
    assert user is not False
    assert user.username == user_data.username


def test_create_access_token():
    user_data = {"sub": "testuser"}
    token = user_service.create_access_token(data=user_data, expires_delta=timedelta(minutes=15))
    payload = jwt.decode(token, "YOUR_SECRET_KEY", algorithms=["HS256"])
    assert payload.get("sub") == "testuser"


def test_get_current_user(mocker, mock_db_session):
    # Mock dependencies required by get_current_user
    mock_user = UserModel(username=user_data.username)
    mocker.patch("services.user_service.get_user", return_value=mock_user)
    mocker.patch(
        "services.user_service.jwt.decode", return_value={"sub": user_data.username}
    )

    # Prepare a fake token
    fake_token = "fake_token"

    # Call the service function with mocked dependencies
    user = user_service.get_current_user(mock_db_session, fake_token)

    # Assertions
    assert user.username == user_data.username
