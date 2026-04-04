import asyncio
from twocaptcha import TwoCaptcha
from app.domain.interfaces.captcha_solver import ISolver
from app.core.config import settings

class TwoCaptchaSolver(ISolver):
    def __init__(self):
        self.solver = TwoCaptcha(settings.TWO_CAPTCHA_API_KEY)

    async def solve(self, site_key: str, url: str) -> str:
        # Since twocaptcha-python is synchronous, we run it in a thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: self.solver.recaptcha(sitekey=site_key, url=url))
        return result['code']
