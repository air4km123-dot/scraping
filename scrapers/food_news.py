"""
Module: food_news — Part 2 (P2W InterPlus).

Food industry: raw materials, meat, production costs, product costs,
shipping costs, new material sources. Google News RSS, same pattern
(and ToS caveat) as scrapers/news.py.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.topic_news import scrape_topic  # noqa: E402

MODULE_NAME = "food_news"
QUERIES = [
    "ต้นทุนวัตถุดิบอาหาร ราคา",
    "ราคาเนื้อหมู เนื้อไก่ วันนี้",
    "ต้นทุนขนส่งสินค้าอาหาร",
    "แหล่งวัตถุดิบอาหารแช่แข็ง ใหม่",
    "อาหารแช่แข็ง ตลาด เทรนด์",
    "ราคาสินค้าเกษตร วัตถุดิบ ปศุสัตว์",
]


def scrape() -> list[dict]:
    return scrape_topic(MODULE_NAME, QUERIES)


if __name__ == "__main__":
    data = scrape()
    print(f"Scraped {len(data)} rows from {MODULE_NAME}")
