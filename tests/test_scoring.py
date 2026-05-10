from datetime import date, datetime, time
from uuid import uuid4
from app.agents.planner import PlannerAgent
from app.agents.scorer import ReservationScoringAgent
from app.db.models import Provider
from app.mcp.schemas import ReservationOpportunity, ReservationTargetCreate


def build_target(auto_book: bool = False, approval: bool = True) -> ReservationTargetCreate:
    return ReservationTargetCreate(
        user_id=uuid4(),
        restaurant_name="Via Carota",
        date_start=date(2026, 6, 1),
        date_end=date(2026, 6, 3),
        time_start=time(19, 0),
        time_end=time(20, 0),
        party_size=2,
        priority=10,
        auto_book=auto_book,
        human_approval_required=approval,
    )


def test_scorer_rewards_exact_match_and_time_window() -> None:
    target = build_target()
    opportunity = ReservationOpportunity(
        provider=Provider.resy,
        restaurant_name="Via Carota",
        reservation_time=datetime(2026, 6, 2, 19, 30),
        party_size=2,
    )
    scored = ReservationScoringAgent().score(target, opportunity)
    assert scored.score >= 0.9
    assert "exact restaurant match" in scored.rationale


def test_planner_auto_books_only_without_human_approval() -> None:
    target = build_target(auto_book=True, approval=False)
    opportunity = ReservationOpportunity(
        provider=Provider.resy,
        restaurant_name="Via Carota",
        reservation_time=datetime(2026, 6, 2, 19, 30),
        party_size=2,
        score=0.95,
    )
    decision = PlannerAgent().decide(target, [opportunity])
    assert decision.action == "book"
