import re
import httpx
import logging
from typing import Optional, Tuple
from playwright.async_api import Page
from app.domain.interfaces.browser import IBrowser
from ..immersive_selectors import SHARE_BTN_SELECTORS, EXTRACT_SHARE_LINK_JS
from ...shopping_constants import SHARE_BTN_TIMEOUT, ESCAPE_KEY, EXPAND_URL_TIMEOUT, PRODUCT_ID_RE, NA_VALUE

logger = logging.getLogger(__name__)

class ProductLinkExtractor:
    @staticmethod
    async def extract(page: Page, browser: IBrowser) -> Tuple[str, str]:
        share_link = await ProductLinkExtractor._extract_share_link(page, browser)
        if not share_link:
            logger.warning("Could not extract share link.")
            return NA_VALUE, NA_VALUE

        product_link = await ProductLinkExtractor._expand_url(share_link)
        product_id = ProductLinkExtractor._extract_product_id(product_link)
        logger.info(f"Found product id: {product_id}")
        return product_link, product_id

    @staticmethod
    async def _extract_share_link(page: Page, browser: IBrowser) -> Optional[str]:
        share_btn = None
        for selector in SHARE_BTN_SELECTORS:
            try:
                share_btn = await page.wait_for_selector(selector, timeout=SHARE_BTN_TIMEOUT)
                if share_btn:
                    break
            except Exception as e:
                logger.info(f"Selector {selector} failed or timed out.", e)
                continue

        if not share_btn:
            logger.warning("Share button not found in side panel.")
            return None

        try:
            await browser.natural_click(page, share_btn)
            await browser.human_delay(2.5, 4.0)
            
            share_link = await page.evaluate(EXTRACT_SHARE_LINK_JS)
            if share_link:
                await page.keyboard.press(ESCAPE_KEY)
                await browser.human_delay(0.5, 1.0)
                logger.info(f"Successfully extracted share link: {share_link}")
                return share_link
        except Exception as e:
            logger.exception("Error extracting share link", e)
        return None

    @staticmethod
    async def _expand_url(url: str) -> str:
        try:
            logger.info(f"Expanding URL: {url}...")
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(url, timeout=EXPAND_URL_TIMEOUT)
                expanded_url = str(response.url)
                logger.info(f"Expanded URL: {expanded_url[:70]}...")
                return expanded_url
        except Exception as e:
            logger.error(f"Error expanding URL {url}", e)
            return url

    @staticmethod
    def _extract_product_id(url: str) -> str:
        if not url or url == NA_VALUE:
            return NA_VALUE
        match = re.search(PRODUCT_ID_RE, url)
        if match:
            return match.group(1)
        return NA_VALUE
