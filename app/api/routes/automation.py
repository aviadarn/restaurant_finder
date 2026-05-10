from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import db_session
from app.db.models import ReservationTarget, TargetStatus

router = APIRouter(prefix="/automation", tags=["automation"])


@router.post("/pause")
async def pause_automation(user_id: UUID, db: AsyncSession = Depends(db_session)) -> dict:
    result = await db.execute(update(ReservationTarget).where(ReservationTarget.user_id == user_id, ReservationTarget.status == TargetStatus.active).values(status=TargetStatus.paused))
    await db.commit()
    return {"paused": result.rowcount}


@router.post("/resume")
async def resume_automation(user_id: UUID, db: AsyncSession = Depends(db_session)) -> dict:
    result = await db.execute(update(ReservationTarget).where(ReservationTarget.user_id == user_id, ReservationTarget.status == TargetStatus.paused).values(status=TargetStatus.active))
    await db.commit()
    if result.rowcount is None:
        raise HTTPException(status_code=500, detail="resume failed")
    return {"resumed": result.rowcount}
