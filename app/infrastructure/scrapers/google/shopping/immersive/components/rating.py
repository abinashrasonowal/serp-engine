import re
import logging
from typing import Optional, Tuple
from playwright.async_api import Locator
from ..immersive_selectors import RATING_SELECTOR, REVIEWS_SELECTOR

logger = logging.getLogger(__name__)

class RatingExtractor:
    @staticmethod
    async def extract(panel: Locator) -> Tuple[Optional[float], Optional[int]]:
        rating, count = None, None
        try:
            # Rating
            r_selector = RATING_SELECTOR
            if r_selector:
                r_element = panel.locator(r_selector).first
                if await r_element.count() > 0:
                    r_text = await r_element.inner_text()
                    r_match = re.search(r'(\d+\.?\d*)', r_text)
                    if r_match:
                        rating = float(r_match.group(1))
                        logger.info(f"Extracted rating: {rating}")
            
            # Reviews (rating_count)
            rev_selector = REVIEWS_SELECTOR
            if rev_selector:
                rev_element = panel.locator(rev_selector).first
                if await rev_element.count() > 0:
                    rev_text = await rev_element.inner_text()
                    count_match = re.search(r'([\d,]+)', rev_text)
                    if count_match:
                        count = int(count_match.group(1).replace(',', ''))
                        logger.info(f"Extracted rating count: {count}")
        except Exception:
            logger.exception("Error extracting rating/reviews from side panel")
            
        return rating, count
