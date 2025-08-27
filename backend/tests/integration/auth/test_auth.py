import pytest


@pytest.mark.asyncio
async def test_me(async_client, test_auth):
    response = await async_client.get("/api/auth/me", cookies=test_auth)
    assert response.status_code == 200
