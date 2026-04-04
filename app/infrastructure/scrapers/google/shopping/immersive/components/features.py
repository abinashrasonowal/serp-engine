import logging
from typing import Any
from playwright.async_api import Locator
from ..immersive_selectors import FEATURES_CONTAINER_SELECTOR

logger = logging.getLogger(__name__)

class FeaturesExtractor:
    @staticmethod
    async def extract(panel: Locator) -> dict[Any, Any]:
        features = {}
        try:
            # This is a simplified implementation. Real-world features are often key-value pairs 
            # in a table or list. We'll look for generic row patterns if possible.
            container = panel.locator(FEATURES_CONTAINER_SELECTOR).first
            if await container.count() > 0:
                # Basic key-value extraction for a typical specs table
                rows = container.locator('tr, div[role="row"]')
                count = await rows.count()
                for i in range(count):
                    row = rows.nth(i)
                    # The new layout uses gridcells for both key and value
                    cells = row.locator('th, td, [role="gridcell"], [role="rowheader"]')
                    cell_count = await cells.count()
                    
                    if cell_count >= 2:
                        key = (await cells.nth(0).inner_text()).strip(': ')
                        val = (await cells.nth(1).inner_text()).strip()
                        features[key] = val
            
            if features:
                logger.info(f"Extracted {len(features)} features.")
            else:
                logger.warning("No features found in container.")
        except Exception as e:
            logger.exception("Error extracting features from side panel", e)
        return features
