import pytest
from app.adapters.outgoing.database import AsyncSessionLocal


@pytest.fixture
async def async_db_session():
    async with AsyncSessionLocal() as session:
        yield session