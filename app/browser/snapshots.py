from pathlib import Path
from playwright.async_api import Page


async def capture_snapshot(page: Page, directory: str, label: str) -> dict[str, str]:
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    png = path / f"{label}.png"
    html = path / f"{label}.html"
    await page.screenshot(path=str(png), full_page=True)
    html.write_text(await page.content(), encoding="utf-8")
    return {"screenshot": str(png), "html": str(html)}
