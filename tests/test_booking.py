from datetime import datetime
from uuid import uuid4
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.db.base import Base
from app.db.models import Booking, BookingStatus, Provider
from app.mcp.schemas import BookingRequest, ReservationOpportunity
from app.services.booking import BookingService


@pytest.mark.asyncio
async def test_duplicate_booking_prevention() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    Session = async_sessionmaker(engine, expire_on_commit=False)
    user_id = uuid4()
    when = datetime(2026, 6, 2, 19, 30)
    async with Session() as session:
        session.add(Booking(user_id=user_id, provider=Provider.resy, restaurant_name="Via Carota", reservation_time=when, party_size=2, status=BookingStatus.confirmed, raw_payload={}))
        await session.commit()
        result = await BookingService().make_booking(
            session,
            BookingRequest(
                user_id=user_id,
                opportunity=ReservationOpportunity(provider=Provider.resy, restaurant_name="Via Carota", reservation_time=when, party_size=2),
                require_human_approval=False,
            ),
        )
    assert result.success is False
    assert "Duplicate" in result.message
