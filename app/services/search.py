from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.browser_executor import BrowserExecutionAgent
from app.agents.scorer import ReservationScoringAgent
from app.mcp.schemas import ReservationOpportunity, ReservationTargetCreate


class ReservationSearchService:
    def __init__(self) -> None:
        self.executor = BrowserExecutionAgent()
        self.scorer = ReservationScoringAgent()

    async def search(self, db: AsyncSession, target: ReservationTargetCreate) -> list[ReservationOpportunity]:
        _ = db
        opportunities = await self.executor.search_all(target)
        return sorted((self.scorer.score(target, item) for item in opportunities), key=lambda item: item.score, reverse=True)
