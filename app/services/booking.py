from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.browser_executor import BrowserExecutionAgent
from app.db.models import Booking, BookingStatus
from app.mcp.schemas import BookingRequest, BookingResult


class BookingService:
    def __init__(self) -> None:
        self.executor = BrowserExecutionAgent()

    async def make_booking(self, db: AsyncSession, request: BookingRequest) -> BookingResult:
        duplicate = await db.scalar(
            select(Booking).where(
                Booking.user_id == request.user_id,
                Booking.provider == request.opportunity.provider,
                Booking.restaurant_name == request.opportunity.restaurant_name,
                Booking.reservation_time == request.opportunity.reservation_time,
                Booking.status != BookingStatus.cancelled,
            )
        )
        if duplicate:
            return BookingResult(success=False, provider=request.opportunity.provider, booking_id=duplicate.id, message="Duplicate active booking prevented")
        if request.require_human_approval:
            return BookingResult(success=False, provider=request.opportunity.provider, message="Human approval required before booking", requires_human_action=True)
        result = await self.executor.make_booking(request.opportunity)
        if result.success:
            booking = Booking(
                user_id=request.user_id,
                target_id=request.target_id,
                provider=request.opportunity.provider,
                restaurant_name=request.opportunity.restaurant_name,
                reservation_time=request.opportunity.reservation_time,
                party_size=request.opportunity.party_size,
                confirmation_code=result.confirmation_code,
                status=BookingStatus.confirmed,
                raw_payload=request.opportunity.raw_payload,
            )
            db.add(booking)
            await db.flush()
            result.booking_id = booking.id
        return result
