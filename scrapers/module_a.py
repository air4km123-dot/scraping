"""
Module A — first scraper (Phase 1).

Placeholder only. Once the target site for Module A is decided, this file
becomes the first real scraper: fetch -> parse -> return a list of
{module, source_url, field, value} rows matching schema/001_init.sql.

Kept deliberately dependency-light (requests + BeautifulSoup) unless the
target site needs JS rendering, in which case swap in Playwright here.
"""

MODULE_NAME = "module_a"


def scrape() -> list[dict]:
    """Return rows shaped for the `scraped_data` table. Not implemented yet —
    fill in once the target URL and fields to track are decided."""
    raise NotImplementedError("Set the target site and fields for module_a first.")


if __name__ == "__main__":
    for row in scrape():
        print(row)
