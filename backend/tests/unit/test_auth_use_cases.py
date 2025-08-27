import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import Response

from src.auth.use_cases.authenticate import authenticate_user
from src.auth.use_cases.log_out import log_out
from src.auth.domain.dtos import AuthRequest
from src.auth.domain.exceptions import IncorrectPassword
from src.users.domain.exceptions import UserNotFound
from src.users.domain.entities import User


@pytest.fixture
def mock_user():
    return User(
        id=1,
        name="user",
        email="test@example.com",
        hashed_password="hashed_password_123",
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )


@pytest.fixture
def mock_auth_request():
    return AuthRequest(username="test@example.com", password="password123")


@pytest.fixture
def mock_dependencies():
    user_uow = AsyncMock()
    user_uow.users = AsyncMock()
    
    pwd_hasher = MagicMock()
    token_service = MagicMock()
    token_repository = AsyncMock()
    
    return {
        "user_uow": user_uow,
        "pwd_hasher": pwd_hasher,
        "token_service": token_service,
        "token_repository": token_repository
    }


@pytest.fixture
def mock_response():
    response = Response()
    response.set_cookie = MagicMock()
    response.delete_cookie = MagicMock()
    return response


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_user, mock_auth_request, mock_dependencies, mock_response):
    """Test successful user authentication"""
    mock_dependencies["user_uow"].users.get_by_email.return_value = mock_user
    mock_dependencies["pwd_hasher"].verify.return_value = True
    mock_dependencies["token_service"].create_access_token.return_value = "access_token_123"
    mock_dependencies["token_service"].create_refresh_token.return_value = "refresh_token_123"

    result = await authenticate_user(
        response=mock_response,
        user_data=mock_auth_request,
        user_uow=mock_dependencies["user_uow"],
        pwd_hasher=mock_dependencies["pwd_hasher"],
        token_service=mock_dependencies["token_service"],
        token_repository=mock_dependencies["token_repository"]
    )

    assert result == {
        "access_token": "access_token_123",
        "refresh_token": "refresh_token_123"
    }
    mock_dependencies["user_uow"].users.get_by_email.assert_called_once_with("test@example.com")
    mock_dependencies["pwd_hasher"].verify.assert_called_once_with(
        password="password123",
        hashed_password="hashed_password_123"
    )
    mock_dependencies["token_service"].create_access_token.assert_called_once_with(mock_user)
    mock_dependencies["token_service"].create_refresh_token.assert_called_once_with(mock_user)
    mock_dependencies["token_repository"].store_refresh_token.assert_called_once_with(1, "refresh_token_123")
    mock_response.set_cookie.assert_any_call(key="users_access_token", value="access_token_123", httponly=False)
    mock_response.set_cookie.assert_any_call(key="users_refresh_token", value="refresh_token_123", httponly=False)


@pytest.mark.asyncio
async def test_authenticate_user_without_cookies(mock_user, mock_auth_request, mock_dependencies, mock_response):
    """Test authentication without setting cookies"""
    mock_dependencies["user_uow"].users.get_by_email.return_value = mock_user
    mock_dependencies["pwd_hasher"].verify.return_value = True
    mock_dependencies["token_service"].create_access_token.return_value = "access_token_123"
    mock_dependencies["token_service"].create_refresh_token.return_value = "refresh_token_123"

    result = await authenticate_user(
        response=mock_response,
        user_data=mock_auth_request,
        user_uow=mock_dependencies["user_uow"],
        pwd_hasher=mock_dependencies["pwd_hasher"],
        token_service=mock_dependencies["token_service"],
        token_repository=mock_dependencies["token_repository"],
        set_cookies=False
    )

    assert result == {
        "access_token": "access_token_123",
        "refresh_token": "refresh_token_123"
    }
    mock_response.set_cookie.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_not_found(mock_auth_request, mock_dependencies, mock_response):
    """Test authentication with a non-existent user"""
    mock_dependencies["user_uow"].users.get_by_email.return_value = None

    with pytest.raises(UserNotFound) as exc_info:
        await authenticate_user(
            response=mock_response,
            user_data=mock_auth_request,
            user_uow=mock_dependencies["user_uow"],
            pwd_hasher=mock_dependencies["pwd_hasher"],
            token_service=mock_dependencies["token_service"],
            token_repository=mock_dependencies["token_repository"]
        )

    assert isinstance(exc_info.value, UserNotFound)
    mock_dependencies["pwd_hasher"].verify.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_incorrect_password(mock_user, mock_auth_request, mock_dependencies, mock_response):
    """Test authentication with an incorrect password"""
    mock_dependencies["user_uow"].users.get_by_email.return_value = mock_user
    mock_dependencies["pwd_hasher"].verify.return_value = False

    with pytest.raises(IncorrectPassword) as exc_info:
        await authenticate_user(
            response=mock_response,
            user_data=mock_auth_request,
            user_uow=mock_dependencies["user_uow"],
            pwd_hasher=mock_dependencies["pwd_hasher"],
            token_service=mock_dependencies["token_service"],
            token_repository=mock_dependencies["token_repository"]
        )

    assert isinstance(exc_info.value, IncorrectPassword)
    mock_dependencies["pwd_hasher"].verify.assert_called_once_with(
        password="password123",
        hashed_password="hashed_password_123"
    )


@pytest.mark.asyncio
async def test_log_out_success(mock_dependencies, mock_response):
    """Test successful logout"""
    current_user_id = 1

    result = await log_out(
        response=mock_response,
        token_repository=mock_dependencies["token_repository"],
        current_user_id=current_user_id
    )

    assert result == {"detail": "Successfully logged out"}
    mock_response.delete_cookie.assert_any_call(key="users_access_token")
    mock_response.delete_cookie.assert_any_call(key="users_refresh_token")
    mock_dependencies["token_repository"].delete_refresh_token.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_log_out_token_repository_error(mock_dependencies, mock_response):
    """Test logout with a repository error"""
    current_user_id = 1
    mock_dependencies["token_repository"].delete_refresh_token.side_effect = Exception("Database error")

    with pytest.raises(Exception) as exc_info:
        await log_out(
            response=mock_response,
            token_repository=mock_dependencies["token_repository"],
            current_user_id=current_user_id
        )

    assert "Database error" in str(exc_info.value)
    mock_response.delete_cookie.assert_any_call(key="users_access_token")
    mock_response.delete_cookie.assert_any_call(key="users_refresh_token")


@pytest.mark.asyncio
async def test_authenticate_user_empty_password(mock_user, mock_dependencies, mock_response):
    """Test authentication with an empty password"""
    user_data = AuthRequest(username="test@example.com", password="")
    mock_dependencies["user_uow"].users.get_by_email.return_value = mock_user
    mock_dependencies["pwd_hasher"].verify.return_value = False

    with pytest.raises(IncorrectPassword):
        await authenticate_user(
            response=mock_response,
            user_data=user_data,
            user_uow=mock_dependencies["user_uow"],
            pwd_hasher=mock_dependencies["pwd_hasher"],
            token_service=mock_dependencies["token_service"],
            token_repository=mock_dependencies["token_repository"]
        )


@pytest.mark.asyncio
async def test_authenticate_user_none_user(mock_auth_request, mock_dependencies, mock_response):
    """Test authentication when the user is None"""
    mock_dependencies["user_uow"].users.get_by_email.return_value = None

    with pytest.raises(UserNotFound):
        await authenticate_user(
            response=mock_response,
            user_data=mock_auth_request,
            user_uow=mock_dependencies["user_uow"],
            pwd_hasher=mock_dependencies["pwd_hasher"],
            token_service=mock_dependencies["token_service"],
            token_repository=mock_dependencies["token_repository"]
        )
