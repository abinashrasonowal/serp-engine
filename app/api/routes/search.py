from fastapi import APIRouter, Depends, HTTPException
from app.domain.interfaces.scraper import IScraper, IParser
from app.domain.interfaces.browser import IBrowser
from app.infrastructure.browser.playwright_browser import PlaywrightBrowser
from app.infrastructure.scrapers.google.shopping.shopping_scraper import GoogleShoppingScraper
from app.infrastructure.scrapers.google.shopping.shopping_parser import GoogleShoppingParser
from app.application.use_cases.search.search_service import GoogleShoppingSearch
from app.application.use_cases.search.search_handler import GoogleShoppingSearchHandler
from app.infrastructure.captcha.two_captcha_solver import TwoCaptchaSolver

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

def get_search_handler(
    search_service: GoogleShoppingSearch = Depends(get_search_service)
) -> GoogleShoppingSearchHandler:
    return GoogleShoppingSearchHandler(search_service)

@router.get("/search")
async def search(
    q: str, 
    handler: GoogleShoppingSearchHandler = Depends(get_search_handler)
):
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
        
    try:
        results = await handler.handle(q)
        return {"query": q, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
