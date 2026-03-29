import json
from playwright.async_api import Page, BrowserContext
from app.core.interfaces.scraper import IScraper
from app.core.interfaces.solver import ISolver
from app.core.interfaces.browser import IBrowser
from typing import Optional, List, Dict, Any

from .google_shopping_selectors import CARD_SELECTORS, SHARE_BTN_SELECTORS, EXTRACT_SHARE_LINK_JS

class GoogleShoppingScraper(IScraper):
    def __init__(self, browser: IBrowser, solver: Optional[ISolver] = None):
        self.browser = browser
        self.solver = solver

    async def scrape(self, query: str) -> str:
        async with self.browser.get_session() as context:
            # We use the existing page or create a new one
            pages = context.pages
            page = pages[0] if pages else await self.browser.create_page(context)
            
            search_url = f"https://www.google.com/search?tbm=shop&q={query}"
            print(f"Navigating to search results...")
            await page.goto(search_url)
            await self.browser.human_delay(2, 4)
            
            await self._handle_captcha(page)
            
            results = await self._process_top_cards(page, search_url)
            return json.dumps(results)

    async def _handle_captcha(self, page: Page):
        if "google.com/sorry" in page.url or await page.query_selector('#captcha-form'):
            print("CAPTCHA detected! Please solve it in the browser window...")
            try:
                await page.wait_for_selector(','.join(CARD_SELECTORS) + ',#search', timeout=120000)
                print("CAPTCHA solved.")
                await self.browser.human_delay(2, 3)
            except Exception:
                print("Timeout waiting for CAPTCHA.")

    async def _get_cards(self, page: Page) -> List[Any]:
        for selector in CARD_SELECTORS:
            elements = await page.query_selector_all(selector)
            if elements:
                return elements
        return []

    async def _process_top_cards(self, page: Page, search_url: str) -> List[Dict[str, str]]:
        print("Identifying cards...")
        results = []
        
        for i in range(10):
            try:
                print(f"Processing card {i+1}/10...")
                cards = await self._get_cards(page)
                
                if not cards or i >= len(cards):
                    if not cards:
                        await page.goto(search_url)
                        await self.browser.human_delay(2, 4)
                        await self._handle_captcha(page)
                        cards = await self._get_cards(page)
                    
                    if i >= len(cards):
                        print(f"   No more cards found at index {i}.")
                        break
                
                card = cards[i]
                await self.browser.natural_scroll(page, card)
                
                aria_label = await card.get_attribute('aria-label') or ""
                title = aria_label.split('.')[0] if aria_label else f"Product {i+1}"
                
                await card.click(force=True)
                await self.browser.human_delay(2.5, 4.0)
                
                share_link = await self._extract_share_link(page)
                
                if share_link:
                    print(f"   Success! Share Link: {share_link}")
                    results.append({"title": title, "link": share_link})
                else:
                    print(f"   Falling back to URL: {page.url}")
                    results.append({"title": title, "link": page.url})

                await page.keyboard.press("Escape")
                await self.browser.human_delay(1.0, 2.0)

            except Exception as e:
                print(f"   Error processing card {i+1}: {e}")
                try: 
                    await page.goto(search_url)
                    await self.browser.human_delay(3, 5)
                except: pass
                continue
                
        return results

    async def _extract_share_link(self, page: Page) -> Optional[str]:
        if "/shopping/product/" in page.url:
            return page.url

        share_btn = None
        for selector in SHARE_BTN_SELECTORS:
            try:
                share_btn = await page.wait_for_selector(selector, timeout=2000)
                if share_btn: break
            except: continue

        if not share_btn:
            return None

        try:
            await self.browser.natural_click(page, share_btn)
            await self.browser.human_delay(2.5, 4.0)
            
            share_link = await page.evaluate(EXTRACT_SHARE_LINK_JS)
            if share_link:
                await page.keyboard.press("Escape")
                await self.browser.human_delay(0.5, 1.0)
                return share_link
        except Exception as e:
            print(f"   Share extraction error: {e}")
            
        return None
