from datetime import date, time
from uuid import UUID
from mcp.server.fastmcp import FastMCP
from app.db.models import Provider
from app.db.session import AsyncSessionLocal
from app.mcp.schemas import BookingRequest, NotificationRequest, ReservationOpportunity, ReservationTargetCreate, WaitlistRequest
from app.mcp import tools

mcp = FastMCP("Reservation Hunter AI")


@mcp.tool()
def describe_tools() -> dict:
    return {
        "tools": [
            "search_reservations", "join_waitlist", "make_booking", "cancel_booking",
            "get_user_preferences", "notify_user", "login_provider", "session_manager",
            "anti_bot_manager", "browser_snapshot", "retry_failed_booking",
        ]
    }


@mcp.tool()
async def search_reservations(user_id: str, restaurant_name: str, date_start: str, date_end: str, time_start: str, time_end: str, party_size: int) -> list[dict]:
    target = ReservationTargetCreate(
        user_id=UUID(user_id),
        restaurant_name=restaurant_name,
        date_start=date.fromisoformat(date_start),
        date_end=date.fromisoformat(date_end),
        time_start=time.fromisoformat(time_start),
        time_end=time.fromisoformat(time_end),
        party_size=party_size,
    )
    async with AsyncSessionLocal() as db:
        return await tools.search_reservations(db, target)


@mcp.tool()
async def join_waitlist(user_id: str, target_id: str, provider: str, restaurant_name: str, requested_date: str, party_size: int) -> dict:
    request = WaitlistRequest(
        user_id=UUID(user_id),
        target_id=UUID(target_id),
        provider=Provider(provider),
        restaurant_name=restaurant_name,
        requested_date=date.fromisoformat(requested_date),
        party_size=party_size,
    )
    async with AsyncSessionLocal() as db:
        result = await tools.join_waitlist(db, request)
        await db.commit()
        return result


@mcp.tool()
async def make_booking(user_id: str, provider: str, restaurant_name: str, reservation_time: str, party_size: int, require_human_approval: bool = True) -> dict:
    opportunity = ReservationOpportunity(
        provider=Provider(provider),
        restaurant_name=restaurant_name,
        reservation_time=reservation_time,
        party_size=party_size,
    )
    request = BookingRequest(user_id=UUID(user_id), opportunity=opportunity, require_human_approval=require_human_approval)
    async with AsyncSessionLocal() as db:
        result = await tools.make_booking(db, request)
        await db.commit()
        return result


@mcp.tool()
async def cancel_booking(booking_id: str) -> dict:
    async with AsyncSessionLocal() as db:
        result = await tools.cancel_booking(db, UUID(booking_id))
        await db.commit()
        return result


@mcp.tool()
async def get_user_preferences(user_id: str) -> dict:
    async with AsyncSessionLocal() as db:
        return await tools.get_user_preferences(db, UUID(user_id))


@mcp.tool()
async def notify_user(user_id: str, channel: str, subject: str, body: str) -> dict:
    async with AsyncSessionLocal() as db:
        result = await tools.notify_user(db, NotificationRequest(user_id=UUID(user_id), channel=channel, subject=subject, body=body))
        await db.commit()
        return result


@mcp.tool()
async def login_provider(user_id: str, provider: str, username: str) -> dict:
    async with AsyncSessionLocal() as db:
        return await tools.login_provider(db, UUID(user_id), Provider(provider), username)


@mcp.tool()
async def session_manager(user_id: str, provider: str) -> dict:
    async with AsyncSessionLocal() as db:
        return await tools.session_manager(db, UUID(user_id), Provider(provider))


@mcp.tool()
def anti_bot_manager(provider: str) -> dict:
    return {"provider": provider, "mode": "compliant_rate_limiting_and_human_handoff", "captcha_bypass": False, "fingerprint_evasion": False}


@mcp.tool()
def browser_snapshot(label: str) -> dict:
    return {"label": label, "status": "snapshot capture available through BrowserManager active page contexts"}


@mcp.tool()
async def retry_failed_booking(booking_id: str) -> dict:
    async with AsyncSessionLocal() as db:
        return await tools.retry_failed_booking(db, UUID(booking_id))


def run() -> None:
    mcp.run()
