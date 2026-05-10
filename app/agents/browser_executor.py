from app.browser.providers import build_provider_registry
from app.db.models import Provider
from app.mcp.schemas import BookingResult, ReservationOpportunity, ReservationTargetCreate, WaitlistRequest


class BrowserExecutionAgent:
    def __init__(self) -> None:
        self.providers = build_provider_registry()

    async def search_all(self, target: ReservationTargetCreate, providers: list[Provider] | None = None) -> list[ReservationOpportunity]:
        selected = providers or list(self.providers)
        results: list[ReservationOpportunity] = []
        for provider in selected:
            results.extend(await self.providers[provider].search_availability(target))
        return results

    async def make_booking(self, opportunity: ReservationOpportunity) -> BookingResult:
        return await self.providers[opportunity.provider].make_booking(opportunity)

    async def join_waitlist(self, request: WaitlistRequest) -> bool:
        return await self.providers[request.provider].join_waitlist(request)

    async def cancel_booking(self, provider: Provider, confirmation_code: str) -> bool:
        return await self.providers[provider].cancel_booking(confirmation_code)
