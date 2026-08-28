"""
Module: karshine — Phase 1 first scraper.

Target: https://www.karshine.com/product (allowed by robots.txt — only
/nogooglebot/ is disallowed). Static server-rendered HTML, paginated via
?page=1..N, ~12 products per page. No login, no JS rendering needed.

Each product yields two rows matching schema/001_init.sql:
  field="product_name"  value=<Thai product name>
  field="price_thb"     value=<numeric price as string>

Run standalone to sanity-check the scrape:
    python scrapers/karshine.py
"""

import re
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MODULE_NAME = "karshine"
BASE_URL = "https://www.karshine.com/product"
REQUEST_DELAY_SECONDS = 1.5  # be polite — don't hammer the site
REQUEST_TIMEOUT_SECONDS = 30
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def _session() -> requests.Session:
    """A session that retries transient network/server errors — daily
    unattended runs (GitHub Actions, Phase 3) shouldn't fail the whole
    module over one dropped connection or a momentary 5xx."""
    session = requests.Session()
    session.headers.update(HEADERS)
    retry = Retry(
        total=3,
        backoff_factor=2,  # 2s, 4s, 8s between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _total_pages(soup: BeautifulSoup) -> int:
    """Read the last page number from the pager (falls back to 1 page)."""
    pager = soup.select_one("p.css-pager")
    if not pager:
        return 1
    page_nums = [int(n) for n in re.findall(r"page=(\d+)", str(pager))]
    return max(page_nums) if page_nums else 1


def _parse_page(soup: BeautifulSoup) -> list[dict]:
    rows = []
    for card in soup.select("div.product_list"):
        link = card.select_one(".product_subject a")
        price_el = card.select_one(".product_price .price_buy")
        if not link or not price_el:
            continue  # skip anything that doesn't match the expected layout

        name = link.get_text(strip=True)
        source_url = link.get("href", BASE_URL)
        price_match = re.search(r"[\d,]+", price_el.get_text())
        price = price_match.group(0).replace(",", "") if price_match else None

        rows.append({
            "module": MODULE_NAME,
            "source_url": source_url,
            "field": "product_name",
            "value": name,
        })
        if price:
            rows.append({
                "module": MODULE_NAME,
                "source_url": source_url,
                "field": "price_thb",
                "value": price,
            })
    return rows


def scrape() -> list[dict]:
    """Fetch every product page and return rows shaped for `scraped_data`."""
    session = _session()

    first_resp = session.get(BASE_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    first_resp.raise_for_status()
    soup = BeautifulSoup(first_resp.text, "html.parser")

    all_rows = _parse_page(soup)
    total_pages = _total_pages(soup)

    for page in range(2, total_pages + 1):
        time.sleep(REQUEST_DELAY_SECONDS)
        resp = session.get(BASE_URL, params={"page": page}, timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        all_rows.extend(_parse_page(BeautifulSoup(resp.text, "html.parser")))

    return all_rows


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
    for row in data[:10]:
        print(row)
