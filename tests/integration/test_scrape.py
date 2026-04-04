import asyncio
import logging
import os
import sys

# Ensure the app directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.scrapers.google.shopping.shopping_scraper import GoogleShoppingScraper
from app.infrastructure.browser.playwright_browser import PlaywrightBrowser
from app.infrastructure.scrapers.google.shopping.shopping_parser import GoogleShoppingParser
from app.domain.interfaces.captcha_solver import ISolver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class MockSolver(ISolver):
    async def solve(self, site_key: str, url: str) -> str:
        logger.info(f"Mocking CAPTCHA solve for {url}")
        return "mocked-token"


async def test_induction_search():
    logger.info("Starting induction search test...")

    # Inject dependencies properly
    browser = PlaywrightBrowser()
    solver = MockSolver()
    scraper = GoogleShoppingScraper(browser=browser, solver=solver)
    parser = GoogleShoppingParser()

    try:
        query = "cooker"
        logger.info(f"Scraping Google Shopping for: {query}")

        # Now returns a SearchResult object
        search_result = await scraper.scrape(query)

        results = search_result.shopping_result
        logger.info(f"Scrape complete. Found {len(results)} results.")

        for i, res in enumerate(results, 1):
            logger.info(f"[{i}] {res.title}")
            logger.info(f"     Position : {res.position}")
            logger.info(f"     ID       : {res.product_id}")
            logger.info(f"     Link     : {res.product_link[:50]}...")
            if res.description != "N/A":
                logger.info(f"     Desc     : {res.description[:100]}...")
            else:
                logger.info("     Desc     : N/A")
            logger.info(f"     Stores   : {len(res.stores)} found")
            if res.features:
                logger.info(f"     Features : {list(res.features.keys())[:5]}")

        if not results:
            logger.warning("No results found. Google might be blocking or the selectors changed.")

    except Exception as e:
        logger.exception(f"An error occurred during testing: {e}")


if __name__ == "__main__":
    asyncio.run(test_induction_search())
