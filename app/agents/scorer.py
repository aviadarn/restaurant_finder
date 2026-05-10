from datetime import datetime, timedelta
from app.mcp.schemas import ReservationOpportunity, ReservationTargetCreate


class ReservationScoringAgent:
    def score(self, target: ReservationTargetCreate, opportunity: ReservationOpportunity) -> ReservationOpportunity:
        score = 0.0
        rationale: list[str] = []
        if opportunity.restaurant_name.lower() == target.restaurant_name.lower():
            score += 0.35
            rationale.append("exact restaurant match")
        elif target.restaurant_name.lower() in opportunity.restaurant_name.lower():
            score += 0.2
            rationale.append("partial restaurant match")

        if target.date_start <= opportunity.reservation_time.date() <= target.date_end:
            score += 0.2
            rationale.append("date in requested range")

        requested_midpoint = datetime.combine(opportunity.reservation_time.date(), target.time_start) + (
            datetime.combine(opportunity.reservation_time.date(), target.time_end) - datetime.combine(opportunity.reservation_time.date(), target.time_start)
        ) / 2
        deviation = abs(opportunity.reservation_time - requested_midpoint)
        if deviation <= timedelta(minutes=target.max_time_deviation_minutes):
            score += 0.25
            rationale.append("time within allowed deviation")
        else:
            score += max(0.0, 0.15 - deviation.total_seconds() / 3600 / 20)
            rationale.append("time outside preferred window")

        if opportunity.party_size == target.party_size:
            score += 0.1
            rationale.append("party size match")
        score += target.priority / 100
        opportunity.score = round(min(score, 1.0), 4)
        opportunity.rationale = "; ".join(rationale)
        return opportunity
