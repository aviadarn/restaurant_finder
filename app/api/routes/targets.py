from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import db_session
from app.db.models import ReservationTarget
from app.mcp.schemas import ReservationTargetCreate

router = APIRouter(prefix="/targets", tags=["targets"])


@router.post("")
async def create_reservation_target(payload: ReservationTargetCreate, db: AsyncSession = Depends(db_session)) -> dict:
    row = ReservationTarget(**payload.model_dump())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return {"id": str(row.id), "status": row.status.value}
