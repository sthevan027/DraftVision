"""FastAPI dependencies for repository and services."""

from collections.abc import AsyncGenerator

from api.core.config import settings
from api.core.database import get_session
from api.core.repository import PostgresRepository
from api.core.storage import AsyncInMemoryStore

# Shared in-memory store for tests / fallback (cleared in test setup)
_memory_store = AsyncInMemoryStore()


async def get_repository() -> AsyncGenerator[PostgresRepository | AsyncInMemoryStore, None]:
    """Provide the appropriate repository (Postgres or InMemory)."""
    if settings.use_memory_store:
        yield _memory_store
        return

    async with get_session() as session:
        yield PostgresRepository(session)
