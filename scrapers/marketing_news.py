"""
Module: marketing_news — Part 2 (P2W InterPlus).

Marketing consulting industry: trends, training courses, events in
Bangkok, related news. Google News RSS, same pattern (and ToS caveat)
as scrapers/news.py.
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
]


def scrape() -> list[dict]:
    return scrape_topic(MODULE_NAME, QUERIES)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
