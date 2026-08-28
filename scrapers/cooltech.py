"""
Module: cooltech — Phase 5.

Target: https://cooltechtechnology.com/en/products/cool-tech-a-c-equipment/
(WordPress/Elementor). robots.txt only disallows /wp-admin/. Each product
is an <h2 class="elementor-heading-title"> inside the products section;
a handful of the same-class headings are section labels rather than
products ("COOL-TECH", "A/C Equipment", "Contact Us") and are filtered
out by name. No prices are shown on this page.

Rows emitted per product:
  field="product_name"  value=<product heading text>
"""

import re

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MODULE_NAME = "cooltech"
BASE_URL = "https://cooltechtechnology.com/en/products/cool-tech-a-c-equipment/"
REQUEST_TIMEOUT_SECONDS = 30
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
# Section labels that share the product heading's CSS class but aren't
# products — keep this list updated if the page layout changes.
NON_PRODUCT_HEADINGS = {"COOL-TECH", "A/C Equipment", "Contact Us"}


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
    for h in soup.select("h2.elementor-heading-title"):
        name = h.get_text(strip=True)
        if not name or name in NON_PRODUCT_HEADINGS:
            continue
        # Same caveat as dynamicair.py: no per-product page here, so a
        # '#slug' fragment keeps each product's source_url distinct —
        # otherwise dedup and the dashboard's per-product grouping would
        # collapse all products sharing this one page into a single row.
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
