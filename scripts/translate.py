"""
Free Thai translation for scraped summaries (news.py, ai_news.py) —
mostly-English article blurbs are otherwise hard to read at a glance.

Uses MyMemory (via deep-translator), a free, no-API-key translation
service — Google Translate's own unofficial endpoint was tried first
and returned no result in testing, MyMemory did. Free tier has a daily
quota per IP, so this only translates text that isn't already
Thai-dominant, to avoid burning quota on text that doesn't need it.
"""

import re

from deep_translator import MyMemoryTranslator

THAI_RANGE = range(0x0E00, 0x0E7F)  # Thai Unicode block
MYMEMORY_MAX_CHARS = 490  # MyMemory rejects requests over ~500 chars
_NON_WORD = re.compile(r"[^\w]+", re.UNICODE)


def is_redundant(summary: str, headline: str) -> bool:
    """True if `summary` doesn't say anything `headline` doesn't already
    say. Google News search results frequently reuse the headline as
    the description, often with only punctuation differences (an
    appended " - Outlet Name", a missing trailing period) — a plain
    string `==` misses those, so this compares on word characters only."""
    norm_summary = _NON_WORD.sub("", summary).lower()
    norm_headline = _NON_WORD.sub("", headline).lower()
    if not norm_summary:
        return True
    return norm_summary in norm_headline or norm_headline in norm_summary


def _is_thai_dominant(text: str, threshold: float = 0.15) -> bool:
    """True if enough of the text is already Thai script that
    translating it again would be pointless (and would waste quota)."""
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    thai_count = sum(1 for c in letters if ord(c) in THAI_RANGE)
    return (thai_count / len(letters)) >= threshold


def to_thai(text: str | None) -> str | None:
    """Translate to Thai if it looks like it needs it; on any failure
    (rate limit, network, unsupported text) fall back to the original
    text rather than dropping the row — a scraper run shouldn't fail
    just because the free translation quota ran out for the day."""
    if not text:
        return text
    if _is_thai_dominant(text):
        return text

    try:
        result = MyMemoryTranslator(source="en-GB", target="th-TH").translate(text[:MYMEMORY_MAX_CHARS])
        return result or text
    except Exception:
        return text
