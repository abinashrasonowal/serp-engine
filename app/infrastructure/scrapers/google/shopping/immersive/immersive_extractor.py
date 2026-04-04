import logging
from playwright.async_api import Page
from app.domain.models.shopping_models import ImmersiveResult
from app.domain.interfaces.browser import IBrowser
from .immersive_selectors import CONTAINER_SELECTOR
from ..shopping_constants import SIDE_PANEL_TIMEOUT, VISIBLE_STATE, NA_VALUE
from .components.title import TitleExtractor
from .components.image import ImageExtractor
from .components.product_url import ProductLinkExtractor
from .components.stores import StoresExtractor
from .components.description import DescriptionExtractor
from .components.features import FeaturesExtractor

logger = logging.getLogger(__name__)

class ImmersiveExtractor:
    @staticmethod
    async def extract_data(page: Page, browser: IBrowser, position: int) -> ImmersiveResult:
        panel = page.locator(CONTAINER_SELECTOR).first
        try:
            await panel.wait_for(state=VISIBLE_STATE, timeout=SIDE_PANEL_TIMEOUT)
        except Exception as e:
            logger.warning("Side panel not found or not visible after timeout.", e)
            return ImmersiveResult(
                title=NA_VALUE,
                product_link=NA_VALUE,
                image_url=NA_VALUE, 
                product_id=NA_VALUE,
                position=position,
                stores=[],
                description=NA_VALUE,
                features={}
            )
        logger.info("Extracting data from side panel...")
        title = await TitleExtractor.extract(panel)
        image_url = await ImageExtractor.extract(panel)
        stores = await StoresExtractor.extract(page)
        description = await DescriptionExtractor.extract(panel)
        features = await FeaturesExtractor.extract(panel)
        product_link, product_id = await ProductLinkExtractor.extract(page, browser)

        return ImmersiveResult(
            title=title,
            image_url=image_url,
            product_link=product_link,
            product_id=product_id,
            position=position,
            stores=stores,
            description=description,
            features=features
        )
