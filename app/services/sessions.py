import json
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.encryption import Encryptor
from app.db.models import Provider, Session


class SessionService:
    def __init__(self, encryptor: Encryptor | None = None) -> None:
        self.encryptor = encryptor or Encryptor()

    async def store_cookie_blob(self, db: AsyncSession, user_id: UUID, provider: Provider, cookies: list[dict], expires_at: datetime | None = None) -> Session:
        encrypted = self.encryptor.encrypt(json.dumps(cookies))
        row = Session(user_id=user_id, provider=provider, encrypted_cookie_blob=encrypted, expires_at=expires_at)
        db.add(row)
        await db.flush()
        return row

    def decrypt_cookie_blob(self, row: Session) -> list[dict]:
        return json.loads(self.encryptor.decrypt(row.encrypted_cookie_blob))
