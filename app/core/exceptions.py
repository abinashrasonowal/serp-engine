class ScraperException(Exception):
    """Base exception for scraper errors."""
    pass


class CaptchaException(ScraperException):
    """Raised when CAPTCHA handling fails."""
    pass


class NoResultsException(ScraperException):
    """Raised when scraping produces no results."""
    pass


class BrowserException(ScraperException):
    """Raised when browser operations fail."""
    pass


class NavigationException(BrowserException):
    """Raised when page navigation fails."""
    pass


class ExtractionException(ScraperException):
    """Raised when data extraction fails."""
    pass
