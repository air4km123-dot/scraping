"""
Module: wise — Phase 5b.

Target: https://wiselubricant.com/shop/ (WooCommerce). robots.txt only
disallows WooCommerce's internal log/upload paths and /wp-admin/ — the
shop listing itself is unrestricted. Standard WooCommerce loop markup,
paginated via /shop/page/N (22 products / 3 pages at time of writing).

Each product yields two rows matching schema/001_init.sql:
  field="product_name"  value=<product name>
  field="price_thb"     value=<numeric price as string>
"""

import re
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MODULE_NAME = "wise"
BASE_URL = "https://wiselubricant.com/shop/"
REQUEST_DELAY_SECONDS = 1.5
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


def _total_pages(soup: BeautifulSoup) -> int:
    pager = soup.select_one("ul.page-numbers")
    if not pager:
        return 1
    nums = [int(a.get_text(strip=True)) for a in pager.select("a.page-numbers, span.page-numbers") if a.get_text(strip=True).isdigit()]
    return max(nums) if nums else 1


def _parse_page(soup: BeautifulSoup) -> list[dict]:
    rows = []
    for item in soup.select("li.product"):
        link = item.select_one("a.woocommerce-loop-product__link")
        title = item.select_one(".woocommerce-loop-product__title")
        price_el = item.select_one(".price .amount")
        if not link or not title:
            continue

        source_url = link.get("href", BASE_URL)
        name = title.get_text(strip=True)
        price = None
        if price_el:
            price_match = re.search(r"[\d,]+(?:\.\d+)?", price_el.get_text())
            if price_match:
                price = price_match.group(0).replace(",", "").split(".")[0]

        rows.append({"module": MODULE_NAME, "source_url": source_url, "field": "product_name", "value": name})
        if price:
            rows.append({"module": MODULE_NAME, "source_url": source_url, "field": "price_thb", "value": price})
    return rows


def scrape() -> list[dict]:
    session = _session()
    first_resp = session.get(BASE_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    first_resp.raise_for_status()
    soup = BeautifulSoup(first_resp.text, "html.parser")

    all_rows = _parse_page(soup)
    total_pages = _total_pages(soup)

    for page in range(2, total_pages + 1):
        time.sleep(REQUEST_DELAY_SECONDS)
        resp = session.get(f"{BASE_URL}page/{page}", timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        all_rows.extend(_parse_page(BeautifulSoup(resp.text, "html.parser")))

    return all_rows


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
    for row in data[:10]:
        print(row)
