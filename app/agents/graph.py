from app.agents.browser_executor import BrowserExecutionAgent
from app.agents.planner import PlanDecision, PlannerAgent
from app.agents.scorer import ReservationScoringAgent
from app.mcp.schemas import ReservationTargetCreate


class ReservationGraph:
    """LangGraph-compatible orchestration boundary.

    The class has explicit async nodes that can be wrapped by LangGraph StateGraph in
    deployments that need durable graph execution.
    """

    def __init__(self) -> None:
        self.executor = BrowserExecutionAgent()
        self.scorer = ReservationScoringAgent()
        self.planner = PlannerAgent()

    async def run_once(self, target: ReservationTargetCreate) -> PlanDecision:
        opportunities = await self.executor.search_all(target)
        scored = [self.scorer.score(target, opportunity) for opportunity in opportunities]
        return self.planner.decide(target, scored)
