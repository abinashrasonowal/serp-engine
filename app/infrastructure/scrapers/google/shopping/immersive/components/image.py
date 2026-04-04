import logging
from playwright.async_api import Locator
from ..immersive_selectors import IMAGE_SELECTOR
from ...shopping_constants import NA_VALUE

logger = logging.getLogger(__name__)

class ImageExtractor:
    @staticmethod
    async def extract(panel: Locator) -> str:
        try:
            selector = IMAGE_SELECTOR
            if not selector:
                logger.warning("Image selector not found.")
                return NA_VALUE
            
            element = panel.locator(selector).first
            if await element.count() > 0:
                val = await element.get_attribute("src")
                if val:
                    logger.info(f"Extracted image URL: {val[:50]}...")
                    return val
            
            logger.warning(f"Image element not found (selector: {selector})")
        except Exception as e:
            logger.exception("Error extracting image from side panel", e)
        return NA_VALUE
