from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.browser_executor import BrowserExecutionAgent
from app.db.models import Booking, BookingStatus


class CancellationService:
    def __init__(self) -> None:
        self.executor = BrowserExecutionAgent()

    async def cancel(self, db: AsyncSession, booking_id: UUID) -> bool:
        booking = await db.get(Booking, booking_id)
        if not booking or not booking.confirmation_code:
            return False
        cancelled = await self.executor.cancel_booking(booking.provider, booking.confirmation_code)
        if cancelled:
            booking.status = BookingStatus.cancelled
            await db.flush()
        return cancelled
