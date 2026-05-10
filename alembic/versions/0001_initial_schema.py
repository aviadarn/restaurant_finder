"""initial reservation hunter schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-10
"""
from collections.abc import Sequence
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

provider = sa.Enum("resy", "opentable", "tock", "sevenrooms", "yelp", "dynamic", name="provider")
target_status = sa.Enum("active", "paused", "completed", "cancelled", name="targetstatus")
booking_status = sa.Enum("pending", "confirmed", "cancelled", "failed", name="bookingstatus")
notification_status = sa.Enum("queued", "sent", "failed", name="notificationstatus")


def upgrade() -> None:
    provider.create(op.get_bind(), checkfirst=True)
    target_status.create(op.get_bind(), checkfirst=True)
    booking_status.create(op.get_bind(), checkfirst=True)
    notification_status.create(op.get_bind(), checkfirst=True)
    op.create_table("users", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("email", sa.String(320), nullable=False), sa.Column("phone", sa.String(32)), sa.Column("telegram_chat_id", sa.String(128)), sa.Column("preferences", sa.JSON(), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("restaurants", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("name", sa.String(255), nullable=False), sa.Column("normalized_name", sa.String(255), nullable=False), sa.Column("neighborhood", sa.String(128)), sa.Column("cuisine", sa.String(128)), sa.Column("popularity_score", sa.Float(), nullable=False), sa.Column("provider", provider), sa.Column("provider_url", sa.Text()), sa.Column("release_metadata", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_restaurants_name", "restaurants", ["name"])
    op.create_index("ix_restaurants_normalized_name", "restaurants", ["normalized_name"])
    op.create_table("reservation_targets", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False), sa.Column("restaurant_name", sa.String(255), nullable=False), sa.Column("restaurant_id", sa.Uuid(), sa.ForeignKey("restaurants.id")), sa.Column("date_start", sa.Date(), nullable=False), sa.Column("date_end", sa.Date(), nullable=False), sa.Column("time_start", sa.Time(), nullable=False), sa.Column("time_end", sa.Time(), nullable=False), sa.Column("party_size", sa.Integer(), nullable=False), sa.Column("neighborhoods", sa.JSON(), nullable=False), sa.Column("cuisines", sa.JSON(), nullable=False), sa.Column("priority", sa.Integer(), nullable=False), sa.Column("max_time_deviation_minutes", sa.Integer(), nullable=False), sa.Column("auto_book", sa.Boolean(), nullable=False), sa.Column("human_approval_required", sa.Boolean(), nullable=False), sa.Column("status", target_status, nullable=False), sa.Column("notification_preferences", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_reservation_targets_user_id", "reservation_targets", ["user_id"])
    op.create_index("ix_reservation_targets_status", "reservation_targets", ["status"])
    op.create_index("ix_reservation_targets_restaurant_name", "reservation_targets", ["restaurant_name"])
    op.create_table("bookings", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False), sa.Column("target_id", sa.Uuid(), sa.ForeignKey("reservation_targets.id")), sa.Column("provider", provider, nullable=False), sa.Column("restaurant_name", sa.String(255), nullable=False), sa.Column("reservation_time", sa.DateTime(timezone=True), nullable=False), sa.Column("party_size", sa.Integer(), nullable=False), sa.Column("confirmation_code", sa.String(128)), sa.Column("status", booking_status, nullable=False), sa.Column("raw_payload", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("user_id", "provider", "restaurant_name", "reservation_time", name="uq_no_duplicate_booking"))
    op.create_index("ix_bookings_user_id", "bookings", ["user_id"])
    op.create_index("ix_bookings_target_id", "bookings", ["target_id"])
    op.create_index("ix_bookings_provider", "bookings", ["provider"])
    op.create_index("ix_bookings_restaurant_name", "bookings", ["restaurant_name"])
    op.create_index("ix_bookings_reservation_time", "bookings", ["reservation_time"])
    op.create_index("ix_bookings_confirmation_code", "bookings", ["confirmation_code"])
    op.create_table("waitlists", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False), sa.Column("target_id", sa.Uuid(), sa.ForeignKey("reservation_targets.id"), nullable=False), sa.Column("provider", provider, nullable=False), sa.Column("restaurant_name", sa.String(255), nullable=False), sa.Column("requested_date", sa.Date(), nullable=False), sa.Column("party_size", sa.Integer(), nullable=False), sa.Column("status", sa.String(64), nullable=False), sa.Column("raw_payload", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_waitlists_user_id", "waitlists", ["user_id"])
    op.create_index("ix_waitlists_target_id", "waitlists", ["target_id"])
    op.create_index("ix_waitlists_provider", "waitlists", ["provider"])
    op.create_table("sessions", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False), sa.Column("provider", provider, nullable=False), sa.Column("encrypted_cookie_blob", sa.Text(), nullable=False), sa.Column("expires_at", sa.DateTime(timezone=True)), sa.Column("healthy", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.create_index("ix_sessions_provider", "sessions", ["provider"])
    op.create_table("provider_accounts", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False), sa.Column("provider", provider, nullable=False), sa.Column("username", sa.String(255), nullable=False), sa.Column("encrypted_refresh_token", sa.Text()), sa.Column("session_id", sa.Uuid(), sa.ForeignKey("sessions.id")), sa.Column("last_login_at", sa.DateTime(timezone=True)), sa.Column("requires_reverification", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_provider_accounts_user_id", "provider_accounts", ["user_id"])
    op.create_index("ix_provider_accounts_provider", "provider_accounts", ["provider"])
    op.create_table("notifications", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False), sa.Column("channel", sa.String(32), nullable=False), sa.Column("subject", sa.String(255), nullable=False), sa.Column("body", sa.Text(), nullable=False), sa.Column("status", notification_status, nullable=False), sa.Column("sent_at", sa.DateTime(timezone=True)), sa.Column("metadata_json", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_table("booking_attempts", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False), sa.Column("target_id", sa.Uuid(), sa.ForeignKey("reservation_targets.id")), sa.Column("provider", provider, nullable=False), sa.Column("status", sa.String(64), nullable=False), sa.Column("score", sa.Float()), sa.Column("error", sa.Text()), sa.Column("raw_payload", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_booking_attempts_user_id", "booking_attempts", ["user_id"])
    op.create_index("ix_booking_attempts_target_id", "booking_attempts", ["target_id"])
    op.create_index("ix_booking_attempts_provider", "booking_attempts", ["provider"])
    op.create_index("ix_booking_attempts_status", "booking_attempts", ["status"])
    op.create_table("audit_logs", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id")), sa.Column("action", sa.String(128), nullable=False), sa.Column("actor", sa.String(128), nullable=False), sa.Column("ip_address", sa.String(64)), sa.Column("metadata_json", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])


def downgrade() -> None:
    for table in ["audit_logs", "booking_attempts", "notifications", "provider_accounts", "sessions", "waitlists", "bookings", "reservation_targets", "restaurants", "users"]:
        op.drop_table(table)
    notification_status.drop(op.get_bind(), checkfirst=True)
    booking_status.drop(op.get_bind(), checkfirst=True)
    target_status.drop(op.get_bind(), checkfirst=True)
    provider.drop(op.get_bind(), checkfirst=True)
