import pytest


@pytest.mark.asyncio
async def test_create_measurement(async_client, auth_headers):
    response = await async_client.post(
        "/api/v1/measurements",
        json={
            "name": "Мои замеры",
            "height": 180,
            "chest": 100,
            "waist": 80,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Мои замеры"
    assert data["data"]["height"] == 180
    assert data["data"]["chest"] == 100
    assert data["data"]["waist"] == 80
    assert data["data"]["is_public"] is False
    assert "share_token" in data["data"]
    assert "id" in data["data"]


@pytest.mark.asyncio
async def test_get_measurements_empty(async_client, auth_headers):
    response = await async_client.get(
        "/api/v1/measurements",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) == 0


@pytest.mark.asyncio
async def test_get_measurements_list(async_client, auth_headers):
    create_response = await async_client.post(
        "/api/v1/measurements",
        json={"name": "Тестовые мерки", "height": 175},
        headers=auth_headers,
    )
    created_id = create_response.json()["data"]["id"]

    response = await async_client.get(
        "/api/v1/measurements",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == created_id
    assert data["data"][0]["name"] == "Тестовые мерки"


@pytest.mark.asyncio
async def test_get_single_measurement(async_client, auth_headers):
    create_response = await async_client.post(
        "/api/v1/measurements",
        json={"name": "Найти меня", "height": 190},
        headers=auth_headers,
    )
    created_id = create_response.json()["data"]["id"]

    response = await async_client.get(
        f"/api/v1/measurements/{created_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == created_id
    assert data["data"]["name"] == "Найти меня"
    assert data["data"]["height"] == 190


@pytest.mark.asyncio
async def test_update_measurement(async_client, auth_headers):

    create_response = await async_client.post(
        "/api/v1/measurements",
        json={"name": "До обновления", "height": 170},
        headers=auth_headers,
    )
    created_id = create_response.json()["data"]["id"]

    response = await async_client.put(
        f"/api/v1/measurements/{created_id}",
        json={"height": 175, "chest": 95},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "До обновления"  # не меняли
    assert data["data"]["height"] == 175  # обновили
    assert data["data"]["chest"] == 95  # добавили


@pytest.mark.asyncio
async def test_delete_measurement(async_client, auth_headers):
    create_response = await async_client.post(
        "/api/v1/measurements",
        json={"name": "Будет удалено", "height": 160},
        headers=auth_headers,
    )
    created_id = create_response.json()["data"]["id"]

    response = await async_client.delete(
        f"/api/v1/measurements/{created_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204

    list_response = await async_client.get(
        "/api/v1/measurements",
        headers=auth_headers,
    )
    data = list_response.json()
    assert len(data["data"]) == 0

    get_response = await async_client.get(
        f"/api/v1/measurements/{created_id}",
        headers=auth_headers,
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_measurement_not_found(async_client, auth_headers):
    response = await async_client.get(
        "/api/v1/measurements/99999",
        headers=auth_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_share_measurement(async_client, auth_headers):
    create_response = await async_client.post(
        "/api/v1/measurements",
        json={"name": "Публичные мерки", "height": 185},
        headers=auth_headers,
    )
    created_id = create_response.json()["data"]["id"]

    share_response = await async_client.post(
        f"/api/v1/measurements/{created_id}/share",
        headers=auth_headers,
    )

    assert share_response.status_code == 200
    share_data = share_response.json()
    assert "share_url" in share_data["data"]

    share_token = share_data["data"]["share_url"].split("/")[-1]

    public_response = await async_client.get(
        f"/api/v1/shared/{share_token}",
    )

    assert public_response.status_code == 200
    public_data = public_response.json()
    assert public_data["data"]["name"] == "Публичные мерки"
    assert public_data["data"]["height"] == 185
    assert "user_id" not in public_data["data"]
    assert "is_public" not in public_data["data"]
    assert "share_token" not in public_data["data"]


@pytest.mark.asyncio
async def test_unauthorized_access(async_client):
    response = await async_client.get("/api/v1/profile")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_public_measurement_not_found(async_client):
    import uuid

    response = await async_client.get(
        f"/api/v1/shared/{uuid.uuid4()}",
    )

    assert response.status_code == 404
