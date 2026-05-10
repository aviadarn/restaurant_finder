from datetime import date, datetime, time
from uuid import UUID
from pydantic import BaseModel, Field
from app.db.models import Provider


class ReservationTargetCreate(BaseModel):
    user_id: UUID
    restaurant_name: str
    date_start: date
    date_end: date
    time_start: time
    time_end: time
    party_size: int = Field(ge=1, le=20)
    neighborhoods: list[str] = Field(default_factory=list)
    cuisines: list[str] = Field(default_factory=list)
    priority: int = Field(default=5, ge=1, le=10)
    max_time_deviation_minutes: int = Field(default=30, ge=0, le=240)
    auto_book: bool = False
    human_approval_required: bool = True
    notification_preferences: dict = Field(default_factory=dict)


class ReservationOpportunity(BaseModel):
    provider: Provider
    restaurant_name: str
    reservation_time: datetime
    party_size: int
    booking_url: str | None = None
    raw_payload: dict = Field(default_factory=dict)
    score: float = 0.0
    rationale: str = ""


class BookingRequest(BaseModel):
    user_id: UUID
    target_id: UUID | None = None
    opportunity: ReservationOpportunity
    require_human_approval: bool = True


class BookingResult(BaseModel):
    success: bool
    provider: Provider
    confirmation_code: str | None = None
    booking_id: UUID | None = None
    message: str
    requires_human_action: bool = False


class WaitlistRequest(BaseModel):
    user_id: UUID
    target_id: UUID
    provider: Provider
    restaurant_name: str
    requested_date: date
    party_size: int


class NotificationRequest(BaseModel):
    user_id: UUID
    channel: str
    subject: str
    body: str
    metadata: dict = Field(default_factory=dict)
