# Google Shopping Scraper API

A robust, SOLID-compliant Google Shopping SERP extraction tool built with FastAPI and Playwright.

## Features
- **Sharable Link Extraction**: Programmatically extracts the top 10 product titles and their `share.google` links.
- **SOLID Architecture**: Decoupled design with abstract interfaces for Scrapers, Parsers, and Browsers.
- **Anti-Bot Protections**: 
  - Persistent browser sessions (cookie management).
  - Randomized human-like delays (jitter).
  - Stealth mode (hiding automation signatures).
- **Manual CAPTCHA Solving**: Waits for the user to solve CAPTCHAs in a non-headless browser.

## Tech Stack
- **Framework**: FastAPI
- **Automation**: Playwright (with Playwright-Stealth)
- **Scraping**: BeautifulSoup4
- **CAPTCHA**: Manual solving with future 2Captcha integration.

## Setup

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/google-shopping-scraper.git
   cd google-shopping-scraper
   ```

2. **Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Environment Configuration**:
   Create a `.env` file:
   ```env
   HEADLESS=False
   USER_DATA_DIR=user_data
   ```

## Usage

### Run the API
```bash
uvicorn app.main:app --reload
```

### Test Extraction Script
```bash
python test_scrape.py
```

## Architecture (Clean Architecture)

- **`app/domain/`**: 
  - `interfaces/`: Core abstractions (IBrowser, IScraper, IParser, ICaptchaSolver).
  - `models/`: Domain entities (SearchResult).
- **`app/application/`**:
  - `use_cases/`: Business orchestration (GoogleShoppingSearch, GoogleShoppingSearchHandler).
- **`app/infrastructure/`**:
  - `browser/`: Playwright implementation.
  - `captcha/`: 2Captcha implementation.
  - `scrapers/google/shopping/`: Specific Google Shopping logic (Scraper, Parser, Selectors).
- **`app/api/`**:
  - `routes/`: FastAPI endpoints.
  - `schemas/`: Request/Response schemas.
