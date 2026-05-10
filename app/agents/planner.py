from dataclasses import dataclass
from app.mcp.schemas import ReservationOpportunity, ReservationTargetCreate


@dataclass(frozen=True)
class PlanDecision:
    action: str
    reason: str
    opportunity: ReservationOpportunity | None = None


class PlannerAgent:
    def decide(self, target: ReservationTargetCreate, opportunities: list[ReservationOpportunity]) -> PlanDecision:
        if not opportunities:
            return PlanDecision("join_waitlist", "No available reservations matched the target")
        best = max(opportunities, key=lambda item: item.score)
        if best.score >= 0.72 and target.auto_book and not target.human_approval_required:
            return PlanDecision("book", "Best opportunity clears auto-book threshold", best)
        if best.score >= 0.55:
            return PlanDecision("request_approval", "Opportunity is viable but requires user approval", best)
        return PlanDecision("wait", "Best opportunity score is below booking threshold", best)
