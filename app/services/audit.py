from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AuditLog


async def audit(session: AsyncSession, action: str, user_id: UUID | None = None, actor: str = "system", metadata: dict | None = None) -> AuditLog:
    row = AuditLog(user_id=user_id, action=action, actor=actor, metadata_json=metadata or {})
    session.add(row)
    await session.flush()
    return row
