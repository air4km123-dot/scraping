"""
Module: solar_news — Part 2 (P2W InterPlus).

Solar cell industry in Thailand: government/support programs, new
product launches, pricing, and top-brand marketing campaigns (general
market intelligence, not specific named competitors — P2W has none
defined for this venture, unlike Air 4's Part 1). Google News RSS,
same pattern (and ToS caveat) as scrapers/news.py.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.topic_news import scrape_topic  # noqa: E402

MODULE_NAME = "solar_news"
QUERIES = [
    "โซล่าเซลล์ ประเทศไทย ข่าว",
    "โครงการโซล่าเซลล์ภาครัฐ",
    "โครงการสนับสนุนโซล่าเซลล์ เงินกู้",
    "โซล่าเซลล์ เปิดตัวสินค้าใหม่",
    "ราคาโซล่าเซลล์ ติดตั้ง",
    "โซล่ารูฟท็อป บ้าน โรงงาน",
    "โซล่าเซลล์ แคมเปญการตลาด แบรนด์ดัง",
    "โซล่าเซลล์ โปรโมชั่น ลดราคา",
]


def scrape() -> list[dict]:
    return scrape_topic(MODULE_NAME, QUERIES)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
