"""
Module: central_events — Part 2 (P2W InterPlus).

Upcoming events and open registrations across Central Thailand
(กรุงเทพฯ and the wider central region, not Bangkok alone), including
contact/registration channels where the article mentions one. Google
News RSS, same pattern (and ToS caveat) as scrapers/news.py.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.topic_news import scrape_topic  # noqa: E402

MODULE_NAME = "central_events"
QUERIES = [
    "งานอีเว้น ภาคกลาง เปิดรับสมัคร",
    "งานอีเว้น กรุงเทพ ปริมณฑล เร็วๆนี้",
    "งานแสดงสินค้า ภาคกลาง",
    "เทศกาล งานประจำปี ภาคกลาง",
    "งานสัมมนา อบรมฟรี กรุงเทพ ภาคกลาง",
]


def scrape() -> list[dict]:
    return scrape_topic(MODULE_NAME, QUERIES)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
