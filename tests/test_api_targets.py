from datetime import date, time
from uuid import uuid4
from app.mcp.schemas import ReservationTargetCreate


def test_reservation_target_schema_accepts_user_inputs() -> None:
    payload = ReservationTargetCreate(
        user_id=uuid4(),
        restaurant_name="Atomix",
        date_start=date(2026, 7, 1),
        date_end=date(2026, 7, 7),
        time_start=time(18, 0),
        time_end=time(21, 0),
        party_size=4,
        neighborhoods=["NoMad"],
        cuisines=["Korean"],
        priority=9,
        max_time_deviation_minutes=45,
        auto_book=True,
        human_approval_required=False,
        notification_preferences={"sms": True},
    )
    assert payload.party_size == 4
    assert payload.auto_book is True
