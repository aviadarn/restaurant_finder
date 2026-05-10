import asyncio
import random
from playwright.async_api import Locator


async def human_delay(min_ms: int = 150, max_ms: int = 900) -> None:
    await asyncio.sleep(random.uniform(min_ms, max_ms) / 1000)


async def human_type(locator: Locator, text: str) -> None:
    for char in text:
        await locator.type(char, delay=random.randint(40, 180))
        if random.random() < 0.08:
            await human_delay(80, 240)
