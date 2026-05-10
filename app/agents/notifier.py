from sqlalchemy.ext.asyncio import AsyncSession
from app.mcp.schemas import NotificationRequest
from app.services.notifications import NotificationService


class NotificationAgent:
    def __init__(self) -> None:
        self.service = NotificationService()

    async def notify(self, db: AsyncSession, request: NotificationRequest):
        return await self.service.enqueue(db, request)
