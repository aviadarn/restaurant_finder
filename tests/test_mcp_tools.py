from app.db.models import Provider
from app.mcp import tools


def test_anti_bot_manager_is_compliance_oriented() -> None:
    import asyncio
    result = asyncio.run(tools.anti_bot_manager(Provider.resy))
    assert result["captcha_bypass"] is False
    assert result["fingerprint_evasion"] is False
