# Immersive Page Selectors
CONTAINER_SELECTOR = 'div[jsname="kefP3d"], div[jsname="HhvoFe"]'
TITLE_SELECTOR = '[data-attrid="product_title"]'
PRICE_RANGE_SELECTOR = '.gayxO, [aria-label^="Typically"]'
RATING_SELECTOR = '.yi40Hd'
REVIEWS_SELECTOR = '.Bk5Fre'
SOURCE_SELECTOR = 'a.uchJRc span.lC5BPc span'
PRODUCT_LINK_SELECTOR = 'a.uchJRc'
IMAGE_SELECTOR = 'img.KfAt4d'

# New UI Selectors
NEW_UI_TITLE_SELECTOR = '[data-attrid="product_title"]'
NEW_UI_RATING_SELECTOR = '[data-attrid="product_rating"] .yi40Hd'
NEW_UI_REVIEWS_SELECTOR = '[data-attrid="product_rating"] .Bk5Fre'
NEW_UI_PRICE_RANGE_SELECTOR = '[aria-label^="Typically"]'
NEW_UI_PLATFORM_SELECTOR = 'a.uchJRc span.lC5BPc span'
NEW_UI_PRODUCT_LINK_SELECTOR = 'a.uchJRc'

# Extended Data Selectors
DESCRIPTION_SELECTOR = '[data-attrid="product_description"] .iERlS, div.P809O, .sh-description__content'
FEATURES_CONTAINER_SELECTOR = '[role="grid"][aria-label="About this product"], .m9376e'
STORES_CONTAINER_SELECTOR = '[data-attrid="organic_offers_grid"], div[jsname="HhvoFe"]'
STORE_ROW_SELECTOR = 'div[jsname="uwagwf"], div[jsname="N6pA9"], .sh-osd__offer-row'
STORE_NAME_SELECTOR = '.hP4iBf, .gUf0b, .OS6vY, .sh-osd__seller-link'
STORE_PRICE_SELECTOR = 'span[aria-label^="Current price"], .JIep9e.GBgquf span, span.H839Ub, .sh-osd__total-price'
STORE_PRODUCT_LINK_SELECTOR = 'a[jsname="wN9W3"], a.P9159d, a.uchJRc, a[jsname="V674He"]'

SHARE_BTN_SELECTORS = [
    'div[aria-label="Share"][role="button"]',
    '.RSNrZe.fXVarf.OJeuxf.btku5b',
    'button[aria-label="Share"]',
    '[aria-label^="Share this product"]'
]

EXTRACT_SHARE_LINK_JS = r"""() => {
    const regex = /https:\/\/share\.google\/[a-zA-Z0-9]+/g;

    // 1. Check jsname="tQ9n1c" specifically (from user HTML)
    const jsnameTarget = document.querySelector('[jsname="tQ9n1c"]');
    if (jsnameTarget && regex.test(jsnameTarget.textContent)) {
        return jsnameTarget.textContent.match(regex)[0];
    }

    // 2. Check input[aria-label="Share link"] (from user HTML)
    const inputTarget = document.querySelector('input[aria-label="Share link"]');
    if (inputTarget && regex.test(inputTarget.value)) {
        return inputTarget.value.match(regex)[0];
    }

    // 3. Fallback: Search all text content
    const match = document.body.textContent.match(regex);
    return match ? match[0] : null;
}"""

