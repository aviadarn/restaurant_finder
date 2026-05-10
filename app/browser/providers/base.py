from abc import ABC, abstractmethod
from app.mcp.schemas import BookingResult, ReservationOpportunity, ReservationTargetCreate, WaitlistRequest


class ProviderAdapter(ABC):
    provider_name: str

    @abstractmethod
    async def search_availability(self, target: ReservationTargetCreate) -> list[ReservationOpportunity]: ...

    @abstractmethod
    async def join_waitlist(self, request: WaitlistRequest) -> bool: ...

    @abstractmethod
    async def make_booking(self, opportunity: ReservationOpportunity) -> BookingResult: ...

    @abstractmethod
    async def cancel_booking(self, confirmation_code: str) -> bool: ...

    @abstractmethod
    async def login(self, username: str, session_hint: str | None = None) -> bool: ...

    @abstractmethod
    async def refresh_session(self) -> bool: ...
