from abc import ABC, abstractmethod
from typing import Dict, Any

class IScraper(ABC):
    @abstractmethod
    async def scrape(self, query: str) -> str:
        """Render the page and return the HTML content."""
        pass

class IParser(ABC):
    @abstractmethod
    def parse(self, html: str) -> Dict[str, Any]:
        """Extract structured data from HTML."""
        pass
