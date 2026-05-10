from datetime import UTC, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Notification, NotificationStatus
from app.mcp.schemas import NotificationRequest


class NotificationService:
    async def enqueue(self, session: AsyncSession, request: NotificationRequest) -> Notification:
        notification = Notification(
            user_id=request.user_id,
            channel=request.channel,
            subject=request.subject,
            body=request.body,
            metadata_json=request.metadata,
        )
        session.add(notification)
        await session.flush()
        return notification

    async def mark_sent(self, notification: Notification) -> Notification:
        notification.status = NotificationStatus.sent
        notification.sent_at = datetime.now(UTC)
        return notification
