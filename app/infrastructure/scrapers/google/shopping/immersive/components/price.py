import re
import logging
from playwright.async_api import Locator
from ..immersive_selectors import PRICE_RANGE_SELECTOR
from ...shopping_constants import NA_VALUE

logger = logging.getLogger(__name__)

class PriceExtractor:
    @staticmethod
    async def extract(panel: Locator) -> str:
        try:
            selector = PRICE_RANGE_SELECTOR
            if not selector:
                logger.warning("Price selector not found.")
                return NA_VALUE
            
            element = panel.locator(selector).first
            if await element.count() > 0:
                text = await element.inner_text()
                if text:
                    price_match = re.search(r'₹([\d,]+)', text)
                    if price_match:
                        price = price_match.group(1).replace(',', '')
                        logger.info(f"Extracted price: {price}")
                        return price
            
            logger.warning(f"Price element not found (selector: {selector})")
        except Exception:
            logger.exception("Error extracting price from side panel")
        return NA_VALUE
