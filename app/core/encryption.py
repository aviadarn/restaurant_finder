import base64
import hashlib
from cryptography.fernet import Fernet
from app.core.config import settings


def _fernet_key(raw: str) -> bytes:
    if raw.startswith("gAAAA") or len(raw) == 44:
        return raw.encode()
    digest = hashlib.sha256(raw.encode()).digest()
    return base64.urlsafe_b64encode(digest)


class Encryptor:
    def __init__(self, key: str | None = None) -> None:
        self._fernet = Fernet(_fernet_key(key or settings.session_encryption_key))

    def encrypt(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self._fernet.decrypt(ciphertext.encode()).decode()
