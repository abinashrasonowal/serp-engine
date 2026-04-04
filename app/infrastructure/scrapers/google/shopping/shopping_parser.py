import re
import json
from bs4 import BeautifulSoup
from app.domain.interfaces.scraper import IParser
from app.domain.models.shopping_models import SearchResult
from typing import List, Dict, Any, Optional
from .shopping_constants import NA_VALUE

class GoogleShoppingParser(IParser):
    def parse(self, data: SearchResult) -> List[Dict[str, Any]]:
        """
        Map SearchResult domain model to a dictionary response for the API.
        """
        try:
            results = []
            for item in data.shopping_result:
                results.append(item.model_dump())
            return results
        except Exception as e:
            print(f"Error mapping SearchResult data: {e}")
            return []