from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import db_session
from app.db.models import User

router = APIRouter(prefix="/preferences", tags=["preferences"])


class PreferenceUpdate(BaseModel):
    user_id: UUID
    preferences: dict = Field(default_factory=dict)


@router.patch("")
async def update_preferences(payload: PreferenceUpdate, db: AsyncSession = Depends(db_session)) -> dict:
    user = await db.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    user.preferences = {**(user.preferences or {}), **payload.preferences}
    await db.commit()
    return {"user_id": str(user.id), "preferences": user.preferences}
