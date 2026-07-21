import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.database import Base, get_session
from app.main import app

TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/measurements_test"
)


@pytest_asyncio.fixture
async def async_client():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    test_async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_session():
        async with test_async_session() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_headers(async_client: AsyncClient):
    phone = "+79991234567"
    await async_client.post("/api/v1/auth/request-code", json={"phone": phone})

    from app.services.auth_service import temp_codes

    code = temp_codes[phone]

    response = await async_client.post(
        "/api/v1/auth/verify-code", json={"phone": phone, "code": code}
    )
    data = response.json()
    access_token = data["data"]["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
