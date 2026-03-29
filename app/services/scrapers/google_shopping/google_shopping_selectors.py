CARD_SELECTORS = ['.njFjte', '.mEooDb', '.sh-dgr__grid-result', '.sh-dlr__list-result']

SHARE_BTN_SELECTORS = [
    'div[aria-label="Share"][role="button"]',
    '.RSNrZe.fXVarf.OJeuxf.btku5b',
    'button[aria-label="Share"]',
    '[aria-label="Share this product"]'
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
