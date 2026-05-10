from playwright.async_api import Page


CAPTCHA_MARKERS = ("captcha", "hcaptcha", "recaptcha", "verify you are human")


async def detect_human_verification(page: Page) -> bool:
    content = (await page.content()).lower()
    return any(marker in content for marker in CAPTCHA_MARKERS)
