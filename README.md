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

## Architecture
- **`app/core/interfaces/`**: Abstract base classes (IScraper, IParser, IBrowser).
- **`app/services/browser/`**: Generic Playwright automation.
- **`app/services/scrapers/google_shopping/`**: Specific search logic.
- **`app/services/google_shopping.py`**: Search orchestrator.

https://github.com/abinashrasonowal/serp-engine.git

git remote add origin https://github.com/abinashrasonowal/serp-engine.git
git branch -M main
git push -u origin main
