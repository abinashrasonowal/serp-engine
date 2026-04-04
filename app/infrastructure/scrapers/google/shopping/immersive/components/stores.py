import logging
from typing import List
from playwright.async_api import Page
from app.domain.models.shopping_models import Store
from ..immersive_selectors import STORE_ROW_SELECTOR, STORE_NAME_SELECTOR, STORE_PRICE_SELECTOR, STORE_PRODUCT_LINK_SELECTOR
from ...shopping_constants import NA_VALUE

logger = logging.getLogger(__name__)

class StoresExtractor:
    @staticmethod
    async def extract(page: Page) -> List[Store]:
        stores = []
        try:
            rows = page.locator(STORE_ROW_SELECTOR)
            count = await rows.count()
            logger.info(f"Identifying stores, found {count} potential rows.")
            
            for i in range(count):
                row = rows.nth(i)
                try:
                    name_el = row.locator(STORE_NAME_SELECTOR).first
                    price_el = row.locator(STORE_PRICE_SELECTOR).first
                    link_el = row.locator(STORE_PRODUCT_LINK_SELECTOR).first
                    
                    name = (await name_el.inner_text()).strip() if await name_el.count() > 0 else NA_VALUE
                    price = (await price_el.inner_text()).strip() if await price_el.count() > 0 else NA_VALUE
                    
                    product_link = NA_VALUE
                    if await link_el.count() > 0:
                        product_link = await link_el.get_attribute("href") or NA_VALUE

                    store = Store(
                        name=name,
                        title=name,
                        link=product_link,
                        price=price,
                        image_url=NA_VALUE,
                        rating=0.0,
                        ratingCount=0
                    )
                    stores.append(store)
                except Exception as e:
                    logger.warning(f"Error extracting store at position {i+1}", e)
                    continue
                    
            logger.info(f"Successfully extracted {len(stores)} stores.")
        except Exception as e:
            logger.exception("Error extracting store list from side panel", e)
        return stores
