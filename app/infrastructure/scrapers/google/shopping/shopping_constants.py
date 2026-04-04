# app/infrastructure/scrapers/google/shopping/shopping_constants.py

# General
NA_VALUE = "NA"
DEFAULT_ENCODING = "utf-8"

# URLs
GOOGLE_SHOPPING_URL_TEMPLATE = "https://www.google.com/search?tbm=shop&q={query}"
CAPTCHA_URL_MARKER = "google.com/sorry"

# Selectors (Common)
CAPTCHA_FORM_SELECTOR = "#captcha-form"
SEARCH_ID_SELECTOR = "#search"

# Playwright Keys/States
ESCAPE_KEY = "Escape"
VISIBLE_STATE = "visible"
NETWORK_IDLE = "networkidle"

# Timeouts (ms)
SIDE_PANEL_TIMEOUT = 5000
SHARE_BTN_TIMEOUT = 2000
EXPAND_URL_TIMEOUT = 10.0 # seconds (for httpx)

# Regex Patterns
PRODUCT_ID_RE = r'catalogid:(\d+)'
