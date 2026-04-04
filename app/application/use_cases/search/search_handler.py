from app.application.use_cases.search.search_service import GoogleShoppingSearch
from typing import List, Dict, Any

class GoogleShoppingSearchHandler:
    def __init__(self, search_service: GoogleShoppingSearch):
        self.search_service = search_service

    async def handle(self, query: str) -> List[Dict[str, Any]]:
        # This wrapper can handle logging, event publishing, or complex mapping
        return await self.search_service.execute(query)
