import asyncio
import os
import sys

# Ensure the app directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.scrapers.google_shopping.google_shopping_scraper import GoogleShoppingScraper
from app.services.browser.playwright import PlaywrightBrowser
from app.services.parser import GoogleShoppingParser
from app.core.interfaces.solver import ISolver

class MockSolver(ISolver):
    async def solve(self, site_key: str, url: str) -> str:
        print(f"Mocking CAPTCHA solve for {url}")
        return "mocked-token"

async def test_induction_search():
    print("Starting induction search test...")
    
    # Inject dependencies properly
    browser = PlaywrightBrowser()
    solver = MockSolver()
    scraper = GoogleShoppingScraper(browser=browser, solver=solver)
    parser = GoogleShoppingParser()
    
    try:
        query = "induction"
        print(f"Scraping Google Shopping for: {query}")
        
        # We need to run this with playwright
        html = await scraper.scrape(query)
        
        print("Scrape complete. Parsing results...")
        results = parser.parse(html)
        
        print(f"Found {len(results)} results:")
        for i, res in enumerate(results, 1):
            print(f"{i}. {res.get('title', 'N/A')}")
            print(f"   Link: {res.get('link', 'N/A')}")
            
        if not results:
            print("No results found. Google might be blocking or the selectors changed.")
            # Let's save the HTML for debugging if no results
            with open("../../debug_google.html", "w") as f:
                f.write(html)
            print("Saved debug_google.html")
            
    except Exception as e:
        print(f"An error occurred during testing: {e}")

if __name__ == "__main__":
    asyncio.run(test_induction_search())
