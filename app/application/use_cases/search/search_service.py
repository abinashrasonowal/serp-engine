from app.domain.interfaces.scraper import IScraper, IParser
from typing import List, Dict, Any

class GoogleShoppingSearch:
    def __init__(self, scraper: IScraper, parser: IParser):
        self.scraper = scraper
        self.parser = parser

    async def execute(self, query: str) -> List[Dict[str, Any]]:
        # 1. Scrape raw data
        raw_data = await self.scraper.scrape(query)
        
        # 2. Parse raw data into structured format
        results = self.parser.parse(raw_data)
        
        return results
