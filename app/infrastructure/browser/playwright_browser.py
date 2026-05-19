import random
import asyncio
from playwright.async_api import async_playwright, Page, BrowserContext
from playwright_stealth import Stealth
from app.core.config import settings
from app.domain.interfaces.browser import IBrowser
import logging
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager
from playwright.async_api import ViewportSize
from urllib.parse import urlparse
import os

logger = logging.getLogger(__name__)

class PlaywrightBrowser(IBrowser):
    def __init__(self, user_data_dir: str = settings.USER_DATA_DIR):
        self.user_data_dir = user_data_dir

    @asynccontextmanager
    async def get_session(self, headless: bool = settings.HEADLESS) -> AsyncGenerator[BrowserContext, None]:
        logger.info(f"Launching local Playwright browser session (headless={headless})...")
        async with async_playwright() as p:
            proxy_config = None
            apify_proxy_password = os.getenv("APIFY_PROXY_PASSWORD")
            
            if apify_proxy_password:
                logger.info("Apify Proxy detected in environment. Using in-built Apify Proxy (Residential)...")
                proxy_config = {
                    "server": "http://proxy.apify.com:8000",
                    "username": "groups-GOOGLE_SERP",
                    "password": apify_proxy_password
                }

            context = await p.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=headless,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport=ViewportSize(width=1440, height=1080),
                args=["--disable-blink-features=AutomationControlled"],
                proxy=proxy_config
            )
            try:
                yield context
            finally:
                logger.info("Closing local Playwright browser session...")
                await context.close()

    async def create_page(self, context: BrowserContext) -> Page:
        page = await context.new_page()
        
        page.on("request", lambda request: logger.info(f"Request started: {request.url}"))
        page.on("requestfailed", lambda request: logger.error(f"Request failed: {request.url} - {request.failure.error_text if request.failure else 'Unknown error'}"))
        page.on("response", lambda response: logger.info(f"Response received: {response.url} - Status: {response.status}"))
        
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
