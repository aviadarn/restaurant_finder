from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Booking, Provider, ReservationTarget, Session, TargetStatus, User
from app.mcp.schemas import BookingRequest, NotificationRequest, ReservationTargetCreate, WaitlistRequest
from app.services.booking import BookingService
from app.services.cancellation import CancellationService
from app.services.notifications import NotificationService
from app.services.search import ReservationSearchService
from app.services.sessions import SessionService
from app.services.waitlist import WaitlistService


async def search_reservations(db: AsyncSession, target: ReservationTargetCreate) -> list[dict]:
    return [item.model_dump(mode="json") for item in await ReservationSearchService().search(db, target)]


async def join_waitlist(db: AsyncSession, request: WaitlistRequest) -> dict:
    row = await WaitlistService().join(db, request)
    return {"waitlist_id": str(row.id), "status": row.status}


async def make_booking(db: AsyncSession, request: BookingRequest) -> dict:
    result = await BookingService().make_booking(db, request)
    return result.model_dump(mode="json")


async def cancel_booking(db: AsyncSession, booking_id: UUID) -> dict:
    return {"cancelled": await CancellationService().cancel(db, booking_id)}


async def get_user_preferences(db: AsyncSession, user_id: UUID) -> dict:
    user = await db.get(User, user_id)
    return user.preferences if user else {}


async def notify_user(db: AsyncSession, request: NotificationRequest) -> dict:
    row = await NotificationService().enqueue(db, request)
    return {"notification_id": str(row.id), "status": row.status.value}


async def login_provider(db: AsyncSession, user_id: UUID, provider: Provider, username: str) -> dict:
    _ = username
    return {"user_id": str(user_id), "provider": provider.value, "status": "manual_verification_required"}


async def session_manager(db: AsyncSession, user_id: UUID, provider: Provider) -> dict:
    row = await db.scalar(select(Session).where(Session.user_id == user_id, Session.provider == provider).order_by(Session.created_at.desc()))
    return {"healthy": bool(row and row.healthy), "expires_at": row.expires_at.isoformat() if row and row.expires_at else None}


async def anti_bot_manager(provider: Provider) -> dict:
    return {"provider": provider.value, "mode": "compliant_rate_limiting_and_human_handoff", "captcha_bypass": False, "fingerprint_evasion": False}


async def browser_snapshot(label: str) -> dict:
    return {"label": label, "status": "snapshot capture available through BrowserManager active page contexts"}


async def retry_failed_booking(db: AsyncSession, booking_id: UUID) -> dict:
    booking = await db.get(Booking, booking_id)
    return {"retryable": bool(booking and booking.status.value == "failed"), "booking_id": str(booking_id)}


async def get_active_searches(db: AsyncSession, user_id: UUID) -> list[ReservationTarget]:
    rows = await db.scalars(select(ReservationTarget).where(ReservationTarget.user_id == user_id, ReservationTarget.status == TargetStatus.active))
    return list(rows)
