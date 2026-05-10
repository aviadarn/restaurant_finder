from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db


async def db_session() -> AsyncIterator[AsyncSession]:
    async for session in get_db():
        yield session
