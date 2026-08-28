"""
Module: wizard — Phase 5b.

Target: https://www.wizardgroup.com/carcare/ — the "car care" product
carousel on Wizard Group's site (Wizard Airklean's parent brand site;
no separate robots.txt restriction found for this path). No WooCommerce
here, no published prices — each item is a carousel card with a product
photo and a caption heading.

The image path (e.g. /assets/product/tyre/stopdog....jpg) is unique per
product and doubles as source_url, since there's no separate product
page to link to.

Rows emitted per product:
  field="product_name"  value=<caption text>
"""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MODULE_NAME = "wizard"
BASE_URL = "https://www.wizardgroup.com/carcare/"
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
    for item in soup.select("#car-care-product li"):
        heading = item.select_one(".caption h5")
        img = item.select_one(".image-wrapp img")
        if not heading or not img:
            continue

        name = heading.get_text(strip=True)
        source_url = urljoin(BASE_URL, img.get("src", ""))
        if not name or not source_url:
            continue

        rows.append({
            "module": MODULE_NAME,
            "source_url": source_url,
            "field": "product_name",
            "value": name,
        })
    return rows


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
    for row in data:
        print(row)
