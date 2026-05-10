from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from playwright.async_api import BrowserContext, Page, async_playwright
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class BrowserManager:
    """Playwright persistent-context manager with compliant session reuse.

    This class intentionally favors provider-respectful automation: persistent sessions,
    conservative pacing, challenge detection, and human handoff rather than CAPTCHA bypass
    or stealth evasion.
    """

    @asynccontextmanager
    async def context(self, user_id: str, provider: str) -> AsyncIterator[BrowserContext]:
        async with async_playwright() as playwright:
            user_data_dir = f"{settings.playwright_user_data_dir}/{user_id}/{provider}"
            logger.info("browser_context_start", provider=provider, user_id=user_id)
            context = await playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=settings.playwright_headless,
                locale="en-US",
                timezone_id="America/New_York",
            )
            try:
                yield context
            finally:
                await context.close()
                logger.info("browser_context_closed", provider=provider, user_id=user_id)

    async def new_page(self, context: BrowserContext) -> Page:
        page = await context.new_page()
        page.set_default_timeout(settings.provider_request_timeout_seconds * 1000)
        return page
