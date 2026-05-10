from datetime import UTC, datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_secret(secret: str) -> str:
    return pwd_context.hash(secret)


def verify_secret(secret: str, hashed: str) -> bool:
    return pwd_context.verify(secret, hashed)


def create_access_token(subject: str, minutes: int = 60) -> str:
    payload = {"sub": subject, "exp": datetime.now(UTC) + timedelta(minutes=minutes)}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
