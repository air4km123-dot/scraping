"""
Module: ai_news — Part 3, "AI อัพเดท".

Tracks newly announced AI models AND new features shipped to existing
ones — what's new, what it can do, what its standout feature is.
Centered on 5 companies: OpenAI (ChatGPT), Google (Gemini/DeepMind),
Anthropic (Claude), Meta AI (Llama), and xAI (Grok) — the first 3 are
the user's named priority, the last 2 are the "2 more prominent
companies" they asked to round it out with. Two source types, same
pattern as news.py:

1. Official company blog RSS — OpenAI, Google AI Blog, Google Gemini
   Blog, DeepMind Blog, Hugging Face Blog. Ordinary outlet feeds, no
   Google-News-style "personal use only" restriction.
2. Google News RSS, queried per major lab/model family, to catch
   coverage of labs without a working RSS feed (Anthropic, Meta AI,
   Mistral, xAI — checked directly; none publish a reachable feed) and
   Thai-language coverage of all of them. Same ToS caveat as the
   news.py module: personal/non-commercial per Google's own feed text,
   used anyway by the same standing user decision as that module.

Rows emitted per article:
  field="headline"      value=<title>
  field="source"         value=<outlet or "Google News: <query>">
  field="published_at"  value=<raw pubDate string>
  field="summary"       value=<description, HTML stripped, truncated,
                         translated to Thai if it wasn't already — see
                         scripts/translate.py>
                         — only when the feed provides one AND it says
                         something the headline doesn't already say
"""

import os
import sys
import time
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Make scripts/ importable regardless of whether this runs standalone
# (python scrapers/ai_news.py) or via scripts/run_module.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.translate import is_redundant, to_thai  # noqa: E402

MODULE_NAME = "ai_news"
REQUEST_TIMEOUT_SECONDS = 30
REQUEST_DELAY_SECONDS = 1.0
SUMMARY_MAX_CHARS = 320
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

# Verified reachable directly (curl): OpenAI, Google AI Blog, Google
# Gemini Blog, DeepMind Blog, Hugging Face Blog. Anthropic, Meta AI,
# and Mistral don't expose a working RSS/Atom feed (404 on every path
# tried) — covered via Google News queries below instead.
OFFICIAL_FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Google AI Blog": "https://blog.google/technology/ai/rss/",
    "Google Gemini Blog": "https://blog.google/products/gemini/rss/",
    "DeepMind Blog": "https://www.deepmind.com/blog/rss.xml",
    "Hugging Face Blog": "https://huggingface.co/blog/feed.xml",
}

GOOGLE_NEWS_QUERIES = [
    # Model launches, per lab/model family
    "Anthropic Claude เปิดตัวโมเดลใหม่",
    "Meta AI Llama เปิดตัว",
    "Mistral AI เปิดตัวโมเดล",
    "xAI Grok เปิดตัว",
    "OpenAI GPT เปิดตัวโมเดลใหม่",
    "Google Gemini เปิดตัวโมเดลใหม่",
    "AI โมเดลใหม่ เปิดตัว ความสามารถ",
    # New-feature coverage specifically, per the 5 companies the user
    # asked to track: ChatGPT/OpenAI, Gemini/Google, Claude/Anthropic,
    # plus Meta AI (Llama) and xAI (Grok) as the "2 more prominent" ones.
    "ChatGPT ฟีเจอร์ใหม่ อัปเดต",
    "OpenAI ฟีเจอร์ใหม่",
    "Gemini ฟีเจอร์ใหม่ อัปเดต",
    "Google AI ฟีเจอร์ใหม่",
    "Claude Anthropic ฟีเจอร์ใหม่",
    "Meta AI Llama ฟีเจอร์ใหม่",
    "Grok xAI ฟีเจอร์ใหม่",
]
GOOGLE_NEWS_ITEMS_PER_QUERY = 4


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
    if not text:
        return None
    return text[:SUMMARY_MAX_CHARS]


def _rows_for_item(item: ET.Element, source_label: str) -> list[dict]:
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
        {"module": MODULE_NAME, "source_url": link, "field": "headline", "value": title},
        {"module": MODULE_NAME, "source_url": link, "field": "source", "value": source_label},
    ]
    published_at = (date_el.text or "").strip() if date_el is not None else ""
    if published_at:
        rows.append({"module": MODULE_NAME, "source_url": link, "field": "published_at", "value": published_at})

    summary = _clean_summary(desc_el.text if desc_el is not None else None)
    # Google News search results often reuse the headline as the whole
    # description — showing that again under the headline is just noise.
    if summary and not is_redundant(summary, title):
        rows.append({"module": MODULE_NAME, "source_url": link, "field": "summary", "value": to_thai(summary)})
    return rows


def _scrape_official_feeds(session: requests.Session) -> list[dict]:
    rows = []
    for outlet_name, feed_url in OFFICIAL_FEEDS.items():
        try:
            resp = session.get(feed_url, timeout=REQUEST_TIMEOUT_SECONDS)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
        except (requests.RequestException, ET.ParseError):
            continue  # one broken feed shouldn't drop every other source

        for item in root.findall(".//item")[:10]:  # each blog's most recent 10 posts
            rows.extend(_rows_for_item(item, outlet_name))
        time.sleep(REQUEST_DELAY_SECONDS)
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
            continue

        for item in root.findall(".//item")[:GOOGLE_NEWS_ITEMS_PER_QUERY]:
            rows.extend(_rows_for_item(item, f"Google News: {query}"))
        time.sleep(REQUEST_DELAY_SECONDS)
    return rows


def scrape() -> list[dict]:
    session = _session()
    return _scrape_official_feeds(session) + _scrape_google_news(session)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
    for row in data[:20]:
        print(row)
