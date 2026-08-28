"""
Module: dynamicair — Phase 5.

Target: https://dynamicair.co.th/ (WordPress/Divi). robots.txt only
disallows /wp-admin/. The homepage has a "สินค้าของบริษัท" (company
products) section with one blurb per product (image + short caption) —
no prices published, so this tracks lineup only, same as ecoair.

The same blurb markup (.et_pb_blurb_description) is reused higher up the
page for a "บริการของบริษัท" (services) section, so the selector below
is scoped to the page's 4th section (et_pb_section_3), which is the
products section specifically — otherwise the two sections' rows mix
together.

Rows emitted per product blurb:
  field="product_name"  value=<blurb caption text>
"""

import re

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MODULE_NAME = "dynamicair"
BASE_URL = "https://dynamicair.co.th/"
PRODUCTS_SECTION_SELECTOR = ".et_pb_section_3 .et_pb_blurb_description"  # see module docstring
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
    for blurb in soup.select(PRODUCTS_SECTION_SELECTOR):
        name = blurb.get_text(strip=True)
        if not name:
            continue
        # This site has no per-product page — every product lives on the
        # same homepage. A '#slug' fragment gives each product a distinct
        # source_url anyway, which the dedup index and the dashboard's
        # per-product grouping both rely on (a shared bare URL would
        # collapse all products into one row).
        # Thai product names have no ASCII to slugify down to, so this only
        # strips whitespace/quotes/slashes rather than lowercasing to a-z0-9.
        slug = re.sub(r"[\s\"'/]+", "-", name).strip("-")
        rows.append({
            "module": MODULE_NAME,
            "source_url": f"{BASE_URL}#{slug}",
            "field": "product_name",
            "value": name,
        })
    return rows


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
    for row in data:
        print(row)
