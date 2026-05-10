import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


class RetryRecoveryAgent:
    async def run(self, operation: Callable[[], Awaitable[T]], attempts: int = 3, base_delay: float = 0.5) -> T:
        last_error: Exception | None = None
        for idx in range(attempts):
            try:
                return await operation()
            except Exception as exc:  # noqa: BLE001 - persisted through booking_attempts by caller
                last_error = exc
                await asyncio.sleep(base_delay * (2**idx))
        raise RuntimeError("operation failed after retries") from last_error
