import asyncio
import os
import sys
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
# Assuming the script is run from project root, or we add absolute path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from app.infrastructure.browser.playwright_browser import PlaywrightBrowser
from app.infrastructure.scrapers.google.shopping.shopping_scraper import GoogleShoppingScraper

async def test_scraper():
    logger.info("Initializing browser...")
    browser = PlaywrightBrowser()
    scraper = GoogleShoppingScraper(browser=browser)
    
    query = "iphone 15"
    logger.info(f"Running scraper for query: {query}")
    
    try:
        # Run scraper
        search_result = await scraper.scrape(query)
        
        logger.info(f"Extracted {len(search_result.shopping_result)} results for query '{search_result.query}'.")
        
        if not search_result.shopping_result:
            logger.error("No results found!")
            return

        for i, res in enumerate(search_result.shopping_result[:5], 1):
            logger.info(f"\nResult {i}:")
            logger.info(f"  Title: {res.title}")
            logger.info(f"  Position: {res.position}")
            logger.info(f"  Image: {res.image_url[:50]}...")
            logger.info(f"  Product Link (Share): {res.product_link}")
            logger.info(f"  Stores: {len(res.stores)} sellers found.")
            logger.info(f"  Description: {res.description[:50]}...")
            
            # Basic validation
            if res.title == "NA":
                logger.warning(f"  Result {i} has 'NA' title.")
            if "google.com/search" in (res.product_link or ""):
                logger.warning(f"  Result {i} product_link looks like a search URL, not a share/product link.")
            elif "google.com/shopping/product/" in (res.product_link or ""):
                logger.info(f"  Result {i} has a valid expanded product link.")

    except Exception as e:
        logger.exception(f"Error during scraping: {e}")

if __name__ == "__main__":
    asyncio.run(test_scraper())
