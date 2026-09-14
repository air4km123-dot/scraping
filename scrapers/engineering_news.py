"""
Module: engineering_news — Part 2 (P2W InterPlus).

Engineering industry: mechanical and other engineering fields,
industry updates, engineering consulting work, training/certification
courses (ใบเซอร์). Google News RSS, same pattern (and ToS caveat) as
scrapers/news.py.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.topic_news import scrape_topic  # noqa: E402

MODULE_NAME = "engineering_news"
QUERIES = [
    "วิศวกรรมเครื่องกล ข่าว",
    "สภาวิศวกร อบรม ใบอนุญาต",
    "ที่ปรึกษาวิศวกรรม งานบริการ",
    "วิศวกรรมโยธา เทรนด์ใหม่",
    "อบรมวิศวกร รับใบเซอร์",
    "วิศวกรรมไฟฟ้า โซล่าเซลล์ ข่าว",
]


def scrape() -> list[dict]:
    return scrape_topic(MODULE_NAME, QUERIES)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
