from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import db_session
from app.db.models import Notification

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
async def get_notifications(user_id: UUID, db: AsyncSession = Depends(db_session)) -> list[dict]:
    rows = await db.scalars(select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc()))
    return [{"id": str(row.id), "channel": row.channel, "subject": row.subject, "status": row.status.value} for row in rows]
