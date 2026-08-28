"""
Module: ecoair — Phase 5.

Target: https://www.ecoairthailand.co.th/ — plain static HTML (no
robots.txt on the site, i.e. nothing declared off-limits). No structured
product-catalog page like Karshine has; the site instead lists its 3
current machine models as nav links on the homepage. That IS the useful
signal here — if a 4th model appears (or one disappears), this row set
changes and that's the "new product launch" signal Part 1 wants tracked
daily. No prices are published anywhere on this site.

Rows emitted per model:
  field="product_name"  value=<model name>
"""

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MODULE_NAME = "ecoair"
BASE_URL = "https://www.ecoairthailand.co.th/"
REQUEST_TIMEOUT_SECONDS = 30
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def _session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    retry = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def scrape() -> list[dict]:
    session = _session()
    resp = session.get(BASE_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []
    seen = set()
    # The product submenu links to product1.php / product2.php / product.php —
    # matching on that filename prefix is what distinguishes them from the
    # rest of the nav (about/contact/etc). The top-level "สินค้า" (Products)
    # menu label points at the same href as the first submenu item, so it's
    # excluded by name — it's a menu label, not a model name.
    for a in soup.select('a[href^="product"]'):
        href = a.get("href", "")
        if not href.startswith("product") or "purifier" in href:
            continue
        name = a.get_text(strip=True)
        if not name or name == "สินค้า" or name in seen:
            continue
        seen.add(name)
        rows.append({
            "module": MODULE_NAME,
            "source_url": BASE_URL + href,
            "field": "product_name",
            "value": name,
        })
    return rows


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
    for row in data:
        print(row)
