from bs4 import BeautifulSoup
from typing import Dict, Any, List
from app.core.interfaces.scraper import IParser

class GoogleShoppingParser(IParser):
    def parse(self, html: str) -> List[Dict[str, Any]]:
        """
        Parses Google Shopping HTML or JSON results.
        Returns a list of products with title, price, and link.
        """
        results = []
        
        # Check if input is JSON (Step 1 implementation returns JSON)
        try:
            import json
            data = json.loads(html)
            if isinstance(data, list):
                return data
        except:
            pass

        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Target Product Cards (Popular options or Grid)
        # Common containers for cards: .mEooDb, .njFjte, .sh-dgr__grid-result, .sh-dlr__list-result
        containers = soup.select('.mEooDb, .njFjte, .sh-dgr__grid-result, .sh-dlr__list-result')
        
        for product in containers[:10]: # Limit to top 10
            # Title extraction
            title_tag = product.select_one('.gkQHve, .XjA7kd, .t7jG0b, h3')
            title = title_tag.get_text(strip=True) if title_tag else "N/A"
            
            # Price extraction
            price_tag = product.select_one('.FG68Ac, .a8U8v, .EY8H7d, span[aria-label*="price"]')
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            
            # Link extraction (The sharable link)
            # We look for links that lead to /shopping/product/
            link_tag = product.select_one('a[href*="/shopping/product/"]')
            if not link_tag:
                # Fallback to any link that looks like a product link
                link_tag = product.select_one('a[href*="/url?url="]')
            
            link = ""
            if link_tag:
                link = link_tag['href']
                if link.startswith('/'):
                    link = f"https://www.google.com{link}"
            
            if title != "N/A":
                results.append({
                    "title": title,
                    "price": price,
                    "link": link
                })
        
        return results
