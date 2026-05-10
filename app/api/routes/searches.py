from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import db_session
from app.db.models import ReservationTarget, TargetStatus

router = APIRouter(prefix="/searches", tags=["searches"])


@router.get("/active")
async def get_active_searches(user_id: UUID, db: AsyncSession = Depends(db_session)) -> list[dict]:
    rows = await db.scalars(select(ReservationTarget).where(ReservationTarget.user_id == user_id, ReservationTarget.status == TargetStatus.active))
    return [{"id": str(row.id), "restaurant_name": row.restaurant_name, "party_size": row.party_size, "status": row.status.value} for row in rows]
