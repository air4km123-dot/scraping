"""
Module: bangkok_events — Part 2 (P2W InterPlus).

Upcoming events and open registrations in Bangkok and nearby
provinces, including contact/registration channels where the article
mentions one. Google News RSS, same pattern (and ToS caveat) as
scrapers/news.py.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.topic_news import scrape_topic  # noqa: E402

MODULE_NAME = "bangkok_events"
QUERIES = [
    "งานอีเว้น กรุงเทพ เปิดรับสมัคร",
    "กิจกรรม กรุงเทพ ปริมณฑล เร็วๆนี้",
    "งานแสดงสินค้า กรุงเทพ",
    "เทศกาล งานออกร้าน กรุงเทพ",
    "งานสัมมนา อบรมฟรี กรุงเทพ",
]


def scrape() -> list[dict]:
    return scrape_topic(MODULE_NAME, QUERIES)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
