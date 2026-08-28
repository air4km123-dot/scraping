"""
Shared runner — scrape a named module and save its rows to Supabase.

This is what both a manual run and the daily GitHub Actions cron
(Phase 3) call, so there's exactly one code path from "run a module" to
"data is in the database."

Usage:
    python scripts/run_module.py karshine
"""

import importlib
import sys

sys.path.insert(0, ".")

from scripts.storage import save_rows  # noqa: E402


def run(module_name: str) -> None:
    scraper = importlib.import_module(f"scrapers.{module_name}")
    rows = scraper.scrape()
    print(f"[{module_name}] scraped {len(rows)} rows")

    sent = save_rows(rows)
    print(f"[{module_name}] sent {sent} rows to Supabase (same-day duplicates skipped automatically)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/run_module.py <module_name>")
        sys.exit(1)
    run(sys.argv[1])
