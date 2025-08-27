from typing import AsyncIterator
from httpx import AsyncClient, ASGITransport
import pytest
import pytest_asyncio
from pytest_asyncio import is_async_test

from src.main import app
from src.users.presentation.dependencies import get_user_uow
from src.tasks.presentation.dependencies import get_task_uow
from src.auth.presentation.dependencies import get_token_repository
from tests.fakes.integration.users import get_test_user_uow
from tests.fakes.integration.tasks import get_test_task_uow
from tests.fakes.integration.auth import get_test_refresh_token_repository


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest.fixture(scope="session")
def user_data() -> dict[str, str | bool]:
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    }


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncIterator:
    app.dependency_overrides[get_user_uow] = get_test_user_uow
    app.dependency_overrides[get_task_uow] = get_test_task_uow
    app.dependency_overrides[get_token_repository] = get_test_refresh_token_repository
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.pop(get_user_uow)
    app.dependency_overrides.pop(get_task_uow)
    app.dependency_overrides.pop(get_token_repository)


@pytest_asyncio.fixture(scope="session")
async def test_user(async_client, user_data):
    response = await async_client.post("/api/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]
    yield user_id
    response = await async_client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204


@pytest_asyncio.fixture(scope="session")
async def test_auth(async_client, test_user, user_data):
    response = await async_client.post("/api/auth/login", json={"username": user_data["email"], "password": user_data["password"]})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    yield response.cookies


@pytest_asyncio.fixture(scope="session")
async def test_task(async_client, test_user, test_auth):
    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "owner_id": test_user,
    }
    response = await async_client.post("/api/tasks", json=task_data, cookies=test_auth)
    assert response.status_code == 201
    task_id = response.json()["id"]
    yield task_id
    response = await async_client.delete(f"/api/tasks/{task_id}", cookies=test_auth)
    assert response.status_code == 204, f"Task deletion failed: {response.text}"
