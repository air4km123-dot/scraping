"""
Module: marketing_news — Part 2 (P2W InterPlus).

Marketing consulting industry: trends, training courses, events in
Bangkok, related news, and top-brand campaigns (general market
intelligence, not specific named competitors — P2W has none defined
for this venture, unlike Air 4's Part 1). Google News RSS, same
pattern (and ToS caveat) as scrapers/news.py.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.topic_news import scrape_topic  # noqa: E402

MODULE_NAME = "marketing_news"
QUERIES = [
    "ที่ปรึกษาการตลาด เทรนด์ใหม่",
    "อบรมการตลาด กรุงเทพ",
    "การตลาดออนไลน์ เทรนด์ 2569",
    "งานอีเว้นการตลาด กทม.",
    "กลยุทธ์การตลาด SME ไทย",
    "แบรนด์ดัง แคมเปญการตลาด ล่าสุด",
]


def scrape() -> list[dict]:
    return scrape_topic(MODULE_NAME, QUERIES)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
