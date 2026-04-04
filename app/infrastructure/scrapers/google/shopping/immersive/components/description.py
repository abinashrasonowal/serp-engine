import logging
from playwright.async_api import Locator
from ..immersive_selectors import DESCRIPTION_SELECTOR
from ...shopping_constants import NA_VALUE

logger = logging.getLogger(__name__)

class DescriptionExtractor:
    @staticmethod
    async def extract(panel: Locator) -> str:
        try:
            element = panel.locator(DESCRIPTION_SELECTOR).first
            if await element.count() > 0:
                text = await element.inner_text()
                if text:
                    text = text.strip()
                    logger.info(f"Extracted description: {text[:50]}...")
                    return text
            
            logger.warning("Description element not found.")
        except Exception as e:
            logger.exception("Error extracting description from side panel", e)
        return NA_VALUE
