import pytest


@pytest.mark.asyncio
async def test_request_code(async_client):
    response = await async_client.post(
        "/api/v1/auth/request-code",
        json={"phone": "+79991234567"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"] is None
    assert data["error"] is None


@pytest.mark.asyncio
async def test_verify_wrong_code(async_client):
    response = await async_client.post(
        "/api/v1/auth/verify-code",
        json={"phone": "+79991234567", "code": "0000"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == 400


@pytest.mark.asyncio
async def test_verify_correct_code(async_client):
    phone = "+79991234567"
    await async_client.post(
        "/api/v1/auth/request-code",
        json={"phone": phone},
    )

    from app.services.auth_service import temp_codes

    code = temp_codes.get(phone)

    response = await async_client.post(
        "/api/v1/auth/verify-code",
        json={"phone": phone, "code": code},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"
