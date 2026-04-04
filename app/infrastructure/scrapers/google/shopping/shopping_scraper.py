import logging
from typing import Optional, List, Any
from playwright.async_api import Page
from app.core.config import settings
from app.domain.interfaces.scraper import IScraper
from app.domain.interfaces.captcha_solver import ISolver
from app.domain.interfaces.browser import IBrowser
from app.domain.models.shopping_models import SearchResult, ImmersiveResult
from .shopping_selectors import CARD_SELECTORS
from .shopping_parser import GoogleShoppingParser
from .immersive.immersive_extractor import ImmersiveExtractor
from .shopping_constants import GOOGLE_SHOPPING_URL_TEMPLATE, CAPTCHA_URL_MARKER, CAPTCHA_FORM_SELECTOR, SEARCH_ID_SELECTOR, ESCAPE_KEY

logger = logging.getLogger(__name__)

class GoogleShoppingScraper(IScraper):
    def __init__(self, browser: IBrowser, solver: Optional[ISolver] = None):
        self.browser = browser
        self.solver = solver
        self.parser = GoogleShoppingParser()
        self.immersive_extractor = ImmersiveExtractor()

    async def scrape(self, query: str) -> SearchResult:
        async with self.browser.get_session() as context:
            pages = context.pages
            page = pages[0] if pages else await self.browser.create_page(context)
            
            search_url = GOOGLE_SHOPPING_URL_TEMPLATE.format(query=query)
            logger.info(f"Navigating to search results: {search_url}")
            await page.goto(search_url)
            await self.browser.human_delay(2, 4)
            
            await self._handle_captcha(page)
            
            results = await self._process_top_cards(page)
            return SearchResult(query=query, shopping_result=results)

    async def _handle_captcha(self, page: Page):
        if CAPTCHA_URL_MARKER in page.url or await page.query_selector(CAPTCHA_FORM_SELECTOR):
            logger.warning("CAPTCHA detected! Please solve it in the browser window...")
            try:
                await page.wait_for_selector(','.join(CARD_SELECTORS) + f',{SEARCH_ID_SELECTOR}', timeout=120000)
                logger.info("CAPTCHA solved.")
                await self.browser.human_delay(2, 3)
            except Exception as e:
                logger.error("Timeout waiting for CAPTCHA solver.", e)

    @staticmethod
    async def _get_cards(page: Page) -> List[Any]:
        for selector in CARD_SELECTORS:
            elements = await page.query_selector_all(selector)
            if elements:
                return elements
        return []

    async def _process_top_cards(self, page: Page) -> List[ImmersiveResult]:
        logger.info("Identifying search result cards...")
        results = []
        
        cards = await self._get_cards(page)
        num_cards = len(cards)
        limit = min(num_cards, settings.MAX_CARDS_TO_PROCESS)
        logger.info(f"Found {num_cards} cards. Processing up to {limit}...")

        for i in range(limit):
            try:
                logger.info(f"Processing card {i+1}/{num_cards}...")
                # Re-fetch cards to ensure we have valid pointers after potential DOM updates
                cards = await self._get_cards(page)
                if i >= len(cards):
                    break
                
                card = cards[i]
                await self.browser.natural_scroll(page, card)

                # 1. Open side panel
                await card.click(force=True)
                await self.browser.human_delay(2.5, 4.0)

                # 2. Extract all details from side panel (including share link and product_id)
                immersive_data = await self.immersive_extractor.extract_data(page, self.browser, i + 1)
                results.append(immersive_data)
                logger.info(f"Successfully extracted: {immersive_data.title[:40]}...")
                
                # Cleanup: Close panel
                await page.keyboard.press(ESCAPE_KEY)
                await self.browser.human_delay(1.5, 2.5)


            except Exception as e:
                logger.exception(f"Error processing card {i+1}", e)
                await page.keyboard.press(ESCAPE_KEY)
                await self.browser.human_delay(1, 2)
                continue
        return results
