from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import db_session
from app.db.models import Booking
from app.services.cancellation import CancellationService

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/{booking_id}/cancel")
async def cancel_booking(booking_id: UUID, db: AsyncSession = Depends(db_session)) -> dict:
    if not await CancellationService().cancel(db, booking_id):
        raise HTTPException(status_code=404, detail="booking not found or cannot be cancelled")
    await db.commit()
    return {"booking_id": str(booking_id), "cancelled": True}


@router.get("/history")
async def get_booking_history(user_id: UUID, db: AsyncSession = Depends(db_session)) -> list[dict]:
    rows = await db.scalars(select(Booking).where(Booking.user_id == user_id).order_by(Booking.reservation_time.desc()))
    return [
        {"id": str(row.id), "restaurant_name": row.restaurant_name, "provider": row.provider.value, "reservation_time": row.reservation_time.isoformat(), "status": row.status.value}
        for row in rows
    ]
