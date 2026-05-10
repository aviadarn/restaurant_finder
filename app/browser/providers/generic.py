import asyncio
from app.db.models import Provider
from app.mcp.schemas import BookingResult, ReservationOpportunity, ReservationTargetCreate, WaitlistRequest
from app.browser.providers.base import ProviderAdapter


class GenericProviderAdapter(ProviderAdapter):
    def __init__(self, provider: Provider) -> None:
        self.provider = provider
        self.provider_name = provider.value

    async def search_availability(self, target: ReservationTargetCreate) -> list[ReservationOpportunity]:
        await asyncio.sleep(0)
        # Provider-specific selectors/API integrations should populate real availability.
        return []

    async def join_waitlist(self, request: WaitlistRequest) -> bool:
        await asyncio.sleep(0)
        return True

    async def make_booking(self, opportunity: ReservationOpportunity) -> BookingResult:
        await asyncio.sleep(0)
        return BookingResult(
            success=True,
            provider=self.provider,
            confirmation_code=f"{self.provider.value.upper()}-DEMO",
            message="Provider adapter accepted booking request",
        )

    async def cancel_booking(self, confirmation_code: str) -> bool:
        await asyncio.sleep(0)
        return bool(confirmation_code)

    async def login(self, username: str, session_hint: str | None = None) -> bool:
        await asyncio.sleep(0)
        return bool(username)

    async def refresh_session(self) -> bool:
        await asyncio.sleep(0)
        return True
