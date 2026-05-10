import enum
import uuid
from datetime import UTC, date, datetime, time
from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Provider(str, enum.Enum):
    resy = "resy"
    opentable = "opentable"
    tock = "tock"
    sevenrooms = "sevenrooms"
    yelp = "yelp"
    dynamic = "dynamic"


class TargetStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    completed = "completed"
    cancelled = "cancelled"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    failed = "failed"


class NotificationStatus(str, enum.Enum):
    queued = "queued"
    sent = "sent"
    failed = "failed"


def now_utc() -> datetime:
    return datetime.now(UTC)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)


class User(TimestampMixin, Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(32))
    telegram_chat_id: Mapped[str | None] = mapped_column(String(128))
    preferences: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    targets: Mapped[list["ReservationTarget"]] = relationship(back_populates="user")


class Restaurant(TimestampMixin, Base):
    __tablename__ = "restaurants"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), index=True)
    neighborhood: Mapped[str | None] = mapped_column(String(128))
    cuisine: Mapped[str | None] = mapped_column(String(128))
    popularity_score: Mapped[float] = mapped_column(Float, default=0.5)
    provider: Mapped[Provider | None] = mapped_column(Enum(Provider))
    provider_url: Mapped[str | None] = mapped_column(Text)
    release_metadata: Mapped[dict] = mapped_column(JSON, default=dict)


class ReservationTarget(TimestampMixin, Base):
    __tablename__ = "reservation_targets"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    restaurant_name: Mapped[str] = mapped_column(String(255), index=True)
    restaurant_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("restaurants.id"))
    date_start: Mapped[date] = mapped_column(Date)
    date_end: Mapped[date] = mapped_column(Date)
    time_start: Mapped[time] = mapped_column(Time)
    time_end: Mapped[time] = mapped_column(Time)
    party_size: Mapped[int] = mapped_column(Integer)
    neighborhoods: Mapped[list[str]] = mapped_column(JSON, default=list)
    cuisines: Mapped[list[str]] = mapped_column(JSON, default=list)
    priority: Mapped[int] = mapped_column(Integer, default=5)
    max_time_deviation_minutes: Mapped[int] = mapped_column(Integer, default=30)
    auto_book: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[TargetStatus] = mapped_column(Enum(TargetStatus), default=TargetStatus.active, index=True)
    notification_preferences: Mapped[dict] = mapped_column(JSON, default=dict)

    user: Mapped[User] = relationship(back_populates="targets")


class Booking(TimestampMixin, Base):
    __tablename__ = "bookings"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    target_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("reservation_targets.id"), index=True)
    provider: Mapped[Provider] = mapped_column(Enum(Provider), index=True)
    restaurant_name: Mapped[str] = mapped_column(String(255), index=True)
    reservation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    party_size: Mapped[int] = mapped_column(Integer)
    confirmation_code: Mapped[str | None] = mapped_column(String(128), index=True)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.pending)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("user_id", "provider", "restaurant_name", "reservation_time", name="uq_no_duplicate_booking"),)


class Waitlist(TimestampMixin, Base):
    __tablename__ = "waitlists"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    target_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reservation_targets.id"), index=True)
    provider: Mapped[Provider] = mapped_column(Enum(Provider), index=True)
    restaurant_name: Mapped[str] = mapped_column(String(255))
    requested_date: Mapped[date] = mapped_column(Date)
    party_size: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(64), default="joined")
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict)


class Session(TimestampMixin, Base):
    __tablename__ = "sessions"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    provider: Mapped[Provider] = mapped_column(Enum(Provider), index=True)
    encrypted_cookie_blob: Mapped[str] = mapped_column(Text)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    healthy: Mapped[bool] = mapped_column(Boolean, default=True)


class ProviderAccount(TimestampMixin, Base):
    __tablename__ = "provider_accounts"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    provider: Mapped[Provider] = mapped_column(Enum(Provider), index=True)
    username: Mapped[str] = mapped_column(String(255))
    encrypted_refresh_token: Mapped[str | None] = mapped_column(Text)
    session_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("sessions.id"))
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    requires_reverification: Mapped[bool] = mapped_column(Boolean, default=False)


class Notification(TimestampMixin, Base):
    __tablename__ = "notifications"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    channel: Mapped[str] = mapped_column(String(32))
    subject: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    status: Mapped[NotificationStatus] = mapped_column(Enum(NotificationStatus), default=NotificationStatus.queued)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)


class BookingAttempt(TimestampMixin, Base):
    __tablename__ = "booking_attempts"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    target_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("reservation_targets.id"), index=True)
    provider: Mapped[Provider] = mapped_column(Enum(Provider), index=True)
    status: Mapped[str] = mapped_column(String(64), index=True)
    score: Mapped[float | None] = mapped_column(Float)
    error: Mapped[str | None] = mapped_column(Text)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict)


class AuditLog(TimestampMixin, Base):
    __tablename__ = "audit_logs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    action: Mapped[str] = mapped_column(String(128), index=True)
    actor: Mapped[str] = mapped_column(String(128), default="system")
    ip_address: Mapped[str | None] = mapped_column(String(64))
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
