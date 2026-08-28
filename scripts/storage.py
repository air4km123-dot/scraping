"""
Shared Supabase writer — every scraper module (karshine.py, and whatever
gets added in Phase 5) calls save_rows() with the same row shape, so the
storage logic lives in exactly one place.
"""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

TABLE = "scraped_data"
# Must match the real columns behind schema/002_scraped_date.sql's
# unique index — this is what makes upsert() skip same-day duplicates
# instead of erroring or inserting a second copy.
ON_CONFLICT = "module,source_url,field,value,scraped_date"


def get_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set — copy "
            ".env.example to .env and fill in real values first."
        )
    return create_client(url, key)


def save_rows(rows: list[dict]) -> int:
    """Upsert rows into `scraped_data`. Rows that collide with today's
    existing (module, source_url, field, value) are silently skipped —
    a rerun of a module on the same day never duplicates history."""
    if not rows:
        return 0

    client = get_client()
    client.table(TABLE).upsert(
        rows,
        on_conflict=ON_CONFLICT,
        ignore_duplicates=True,
    ).execute()
    return len(rows)
