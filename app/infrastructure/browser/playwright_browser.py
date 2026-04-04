import random
import asyncio
from playwright.async_api import async_playwright, Page, BrowserContext
from playwright_stealth import Stealth
from app.core.config import settings
from app.domain.interfaces.browser import IBrowser
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager
from playwright.async_api import ViewportSize

class PlaywrightBrowser(IBrowser):
    def __init__(self, user_data_dir: str = settings.USER_DATA_DIR):
        self.user_data_dir = user_data_dir

    @asynccontextmanager
    async def get_session(self, headless: bool = settings.HEADLESS) -> AsyncGenerator[BrowserContext, None]:
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=headless,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport=ViewportSize(width=1440, height=1080),
                args=["--disable-blink-features=AutomationControlled"]
            )
            try:
                yield context
            finally:
                await context.close()

    async def create_page(self, context: BrowserContext) -> Page:
        page = await context.new_page()
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        return page

    async def human_delay(self, min_s: float = 1.0, max_s: float = 3.0):
        await asyncio.sleep(random.uniform(min_s, max_s))

    async def natural_scroll(self, page: Page, element: Any):
        await element.evaluate("el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })")
        await self.human_delay(0.5, 1.5)

    async def natural_click(self, page: Page, element: Any):
        box = await element.bounding_box()
        if box:
            await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=5)
        await element.click(force=True)
