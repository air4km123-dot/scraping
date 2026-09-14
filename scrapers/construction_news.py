"""
Module: construction_news — Part 2 (P2W InterPlus).

Construction/renovation industry: home building, renovation, materials
(steel, cement, sand/gravel), decor materials, bank/government support
programs, and top-brand marketing campaigns (general market
intelligence, not specific named competitors — P2W has none defined
for this venture, unlike Air 4's Part 1). Google News RSS, same
pattern (and ToS caveat) as scrapers/news.py.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.topic_news import scrape_topic  # noqa: E402

MODULE_NAME = "construction_news"
QUERIES = [
    "ข่าวก่อสร้าง ต่อเติมบ้าน รีโนเวท",
    "ราคาวัสดุก่อสร้าง ปูน เหล็ก",
    "ราคาทราย หิน ก่อสร้าง",
    "วัสดุตกแต่งบ้าน เทรนด์ใหม่",
    "สินเชื่อสร้างบ้าน ต่อเติม ธนาคาร",
    "โครงการภาครัฐ สนับสนุนสร้างบ้าน",
    "วัสดุก่อสร้าง แคมเปญการตลาด แบรนด์ดัง",
    "ผู้รับเหมา ก่อสร้าง โปรโมชั่น ลูกค้า",
]


def scrape() -> list[dict]:
    return scrape_topic(MODULE_NAME, QUERIES)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
