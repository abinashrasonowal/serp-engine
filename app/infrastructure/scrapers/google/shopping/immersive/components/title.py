import logging
from playwright.async_api import Locator
from ..immersive_selectors import TITLE_SELECTOR
from ...shopping_constants import NA_VALUE

logger = logging.getLogger(__name__)

class TitleExtractor:
    @staticmethod
    async def extract(panel: Locator) -> str:
        try:
            selector = TITLE_SELECTOR
            if not selector:
                logger.warning("Title selector not found.")
                return NA_VALUE
            
            element = panel.locator(selector).first
            if await element.count() > 0:
                text = await element.inner_text()
                if text:
                    text = text.strip()
                    logger.info(f"Extracted title: {text}")
                    return text
            
            logger.warning(f"Title element not found (selector: {selector})")
        except Exception as e:
            logger.exception("Error extracting title from side panel", e)
        return NA_VALUE
