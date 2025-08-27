import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_update_task(async_client, test_auth, test_task):
    response = await async_client.patch(f"/api/tasks/{test_task}", json={"title": "Updated Test Task"}, cookies=test_auth)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Task"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_task(async_client, test_auth, test_task):
    response = await async_client.get(f"/api/tasks/{test_task}", cookies=test_auth)
    assert response.status_code == 200
    assert response.json()["id"] == test_task
