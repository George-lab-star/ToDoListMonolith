import pytest


input_data = {
    "name": "John",
    "email": "john@example.com",
    "password": "secuerepassword",
    "is_active": True,
    "is_superuser": False,
    "is_verified": False
}


@pytest.mark.asyncio
async def test_create_user(async_client):
    response = await async_client.post("/api/users", json=input_data)
    assert response.status_code == 201
    assert response.json()["name"] == "John"


@pytest.mark.asyncio
async def test_get_user(async_client, test_user):
    response = await async_client.get(f"api/users/{test_user}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user(async_client, test_user):
    response = await async_client.patch(f"/api/users/{test_user}", json={"name": "John Doe"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
