"""
Shared Google News RSS scraper for Part 2 (P2W InterPlus) industry-news
modules — solar, construction, engineering, marketing, food, events.

Same source and pattern as scrapers/news.py's Google News half (same
ToS caveat: Google's feed text says "personal, non-commercial use",
used anyway per the same standing user decision), factored out here so
each topic module is just a short list of search queries instead of
six copies of the same scraping code.

Rows emitted per article:
  field="headline"      value=<title>
  field="source"        value=<"Google News: <query>">
  field="published_at"  value=<raw pubDate string>
  field="summary"       value=<description, HTML stripped, translated
                         to Thai if it wasn't already — see
                         scripts/translate.py> — only when the feed
                         provides one AND it says something the
                         headline doesn't already say
"""

import time
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from scripts.translate import is_redundant, to_thai

REQUEST_TIMEOUT_SECONDS = 30
REQUEST_DELAY_SECONDS = 1.0
SUMMARY_MAX_CHARS = 320
DEFAULT_ITEMS_PER_QUERY = 5
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


def _clean_summary(raw_html: str | None) -> str | None:
    if not raw_html:
        return None
    text = BeautifulSoup(raw_html, "html.parser").get_text(" ", strip=True)
    return text[:SUMMARY_MAX_CHARS] if text else None


def _rows_for_item(module_name: str, item: ET.Element, source_label: str) -> list[dict]:
    title_el = item.find("title")
    link_el = item.find("link")
    date_el = item.find("pubDate")
    desc_el = item.find("description")
    if title_el is None or link_el is None or not (link_el.text or "").strip():
        return []

    title = (title_el.text or "").strip()
    link = link_el.text.strip()
    if not title:
        return []

    rows = [
        {"module": module_name, "source_url": link, "field": "headline", "value": title},
        {"module": module_name, "source_url": link, "field": "source", "value": source_label},
    ]
    published_at = (date_el.text or "").strip() if date_el is not None else ""
    if published_at:
        rows.append({"module": module_name, "source_url": link, "field": "published_at", "value": published_at})

    summary = _clean_summary(desc_el.text if desc_el is not None else None)
    if summary and not is_redundant(summary, title):
        rows.append({"module": module_name, "source_url": link, "field": "summary", "value": to_thai(summary)})
    return rows


def scrape_topic(module_name: str, queries: list[str], items_per_query: int = DEFAULT_ITEMS_PER_QUERY) -> list[dict]:
    session = _session()
    rows = []
    for query in queries:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=th&gl=TH&ceid=TH:th"
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
        except (requests.RequestException, ET.ParseError):
            continue  # one bad query shouldn't drop every other query's results

        for item in root.findall(".//item")[:items_per_query]:
            rows.extend(_rows_for_item(module_name, item, f"Google News: {query}"))
        time.sleep(REQUEST_DELAY_SECONDS)
    return rows
