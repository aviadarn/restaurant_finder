from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.browser_executor import BrowserExecutionAgent
from app.db.models import Waitlist
from app.mcp.schemas import WaitlistRequest


class WaitlistService:
    def __init__(self) -> None:
        self.executor = BrowserExecutionAgent()

    async def join(self, db: AsyncSession, request: WaitlistRequest) -> Waitlist:
        await self.executor.join_waitlist(request)
        row = Waitlist(**request.model_dump(), raw_payload={})
        db.add(row)
        await db.flush()
        return row
