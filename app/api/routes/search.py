from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.core.interfaces.scraper import IScraper, IParser
from app.core.interfaces.browser import IBrowser
from app.services.browser.playwright import PlaywrightBrowser
from app.services.scrapers.google_shopping.google_shopping_scraper import GoogleShoppingScraper
from app.services.parser import GoogleShoppingParser
from app.services.google_shopping import GoogleShoppingSearch
from app.services.captcha_solvers.two_captcha import TwoCaptchaSolver

router = APIRouter()

def get_browser() -> IBrowser:
    return PlaywrightBrowser()

def get_scraper(browser: IBrowser = Depends(get_browser)) -> IScraper:
    solver = TwoCaptchaSolver()
    return GoogleShoppingScraper(browser=browser, solver=solver)

def get_parser() -> IParser:
    return GoogleShoppingParser()

def get_search_service(
    scraper: IScraper = Depends(get_scraper),
    parser: IParser = Depends(get_parser)
) -> GoogleShoppingSearch:
    return GoogleShoppingSearch(scraper, parser)

@router.get("/search")
async def search(
    q: str, 
    search_service: GoogleShoppingSearch = Depends(get_search_service)
):
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
        
    try:
        results = await search_service.execute(q)
        return {"query": q, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
