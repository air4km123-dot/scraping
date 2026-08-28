"""
Module: news — Phase "ข่าวอัพเดท" (news/market trend tracking).

Two sources, combined so an article missed by one still shows up via
the other:

1. Google News RSS, queried per competitor name (+ a couple of
   industry-wide terms). Free and unrestricted to fetch, but Google's
   own feed copyright notice limits it to "personal, non-commercial
   use in a feed reader" — flagged to the user, who chose to proceed
   knowing that.
2. Direct outlet RSS — Thairath and Prachachat's own official feeds
   (ordinary WordPress/CMS RSS, no such restriction). These are
   general news feeds, not searchable, so this module filters their
   items locally for anything mentioning a tracked competitor or an
   industry keyword.

Rows emitted per matched article:
  field="headline"      value=<article title>
  field="source"        value=<"Google News: <query>" or the outlet name>
  field="published_at"  value=<raw pubDate string from the feed>
"""

import time
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MODULE_NAME = "news"
REQUEST_TIMEOUT_SECONDS = 30
REQUEST_DELAY_SECONDS = 1.0
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

# The 10 named direct competitors (see project memory) plus a couple of
# industry-wide terms so broader market/regulatory news gets caught too.
GOOGLE_NEWS_QUERIES = [
    # Generic-sounding brand names ("Freshair", "Eco Air", "Cool Tech", "U
    # Cool") collide with unrelated home-AC/appliance news unless pinned
    # down with "รถยนต์" (car) — verified: without it, "Freshair" matched a
    # TCL home air conditioner feature and "Eco Air" matched a Xiaomi one.
    "Freshair ล้างแอร์รถยนต์",
    "Eco Air ล้างแอร์รถยนต์",
    "WISE เครื่องล้างแอร์",
    "Wizard Airklean",
    "Karshine",
    "Speedclean ล้างแอร์รถยนต์",
    "Cool Tech ล้างแอร์รถยนต์",
    "U Cool ล้างแอร์รถยนต์",
    "Dynamicair OR Dynatech เครื่องล้างแอร์",
    "NWP แอร์ซัพพลาย",
    "เครื่องล้างแอร์รถยนต์ไม่ถอดตู้",
    "น้ำยาล้างหัวฉีดรถยนต์",
]
GOOGLE_NEWS_ITEMS_PER_QUERY = 4

# Keywords used to filter the general outlet feeds down to relevant items.
OUTLET_KEYWORDS = [
    "เครื่องล้างแอร์", "น้ำยาล้างแอร์", "ล้างหัวฉีด", "ล้างห้องเครื่อง",
    "ล้างเบรก", "ศูนย์บริการรถยนต์", "Toyota", "โตโยต้า", "Isuzu", "อีซูซุ",
    "Freshair", "Eco Air", "WISE", "Wizard Airklean", "Karshine",
    "Speedclean", "Cool Tech", "U Cool", "Dynamicair", "Dynatech", "NWP",
]
OUTLET_FEEDS = {
    "Thairath": "https://www.thairath.co.th/rss/news",
    "Prachachat": "https://www.prachachat.net/feed",
}

RSS_NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def _session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    retry = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _rows_for_item(item: ET.Element, source_label: str) -> list[dict]:
    title_el = item.find("title")
    link_el = item.find("link")
    date_el = item.find("pubDate")
    if title_el is None or link_el is None or not (link_el.text or "").strip():
        return []

    title = (title_el.text or "").strip()
    link = link_el.text.strip()
    published_at = (date_el.text or "").strip() if date_el is not None else ""
    if not title:
        return []

    rows = [
        {"module": MODULE_NAME, "source_url": link, "field": "headline", "value": title},
        {"module": MODULE_NAME, "source_url": link, "field": "source", "value": source_label},
    ]
    if published_at:
        rows.append({"module": MODULE_NAME, "source_url": link, "field": "published_at", "value": published_at})
    return rows


def _scrape_google_news(session: requests.Session) -> list[dict]:
    rows = []
    for query in GOOGLE_NEWS_QUERIES:
        url = f"https://news.google.com/rss/search?q={quote(query)}&hl=th&gl=TH&ceid=TH:th"
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
        except (requests.RequestException, ET.ParseError):
            continue  # one bad query shouldn't drop every other query's results

        items = root.findall(".//item")[:GOOGLE_NEWS_ITEMS_PER_QUERY]
        for item in items:
            rows.extend(_rows_for_item(item, f"Google News: {query}"))
        time.sleep(REQUEST_DELAY_SECONDS)
    return rows


def _scrape_outlets(session: requests.Session) -> list[dict]:
    rows = []
    for outlet_name, feed_url in OUTLET_FEEDS.items():
        try:
            resp = session.get(feed_url, timeout=REQUEST_TIMEOUT_SECONDS)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
        except (requests.RequestException, ET.ParseError):
            continue

        for item in root.findall(".//item"):
            title_el = item.find("title")
            title = (title_el.text or "") if title_el is not None else ""
            if not any(keyword.lower() in title.lower() for keyword in OUTLET_KEYWORDS):
                continue  # not relevant to our competitors/industry — skip
            rows.extend(_rows_for_item(item, outlet_name))
        time.sleep(REQUEST_DELAY_SECONDS)
    return rows


def scrape() -> list[dict]:
    session = _session()
    return _scrape_google_news(session) + _scrape_outlets(session)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
    for row in data[:20]:
        print(row)
