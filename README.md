# scraping — Strategic Data Intelligence Pipeline

Daily-refreshed, multi-module web scraping pipeline. Each topic page runs as
its own scraper module; all modules write into one shared database and feed
one dashboard. Built to run on free-tier infrastructure only.

## Status

- [x] Phase 0 — repo & schema
- [ ] Phase 1 — first scraper module
- [ ] Phase 2 — storage & dedup
- [ ] Phase 3 — daily automation (GitHub Actions cron)
- [ ] Phase 4 — dashboard v1
- [ ] Phase 5 — remaining modules
- [ ] Phase 6 — failure monitoring & alerts

## Project layout

```
scrapers/     one file per module (module_a.py, module_b.py, ...)
schema/       versioned SQL migrations, run in order against Supabase/Postgres
scripts/      one-off / shared utilities (e.g. backup, dedup helpers)
.github/workflows/   cron jobs that run each scraper on schedule
```

## Setup

1. Copy `.env.example` to `.env` and fill in real values. `.env` is
   gitignored — never commit real keys.
2. `pip install -r requirements.txt`
3. Apply `schema/001_init.sql` to your Supabase/Postgres database.

## Portability note

No API keys or connection strings are hardcoded anywhere in this repo — they
all come from environment variables (`.env` locally, GitHub Actions Secrets
in CI, Vercel env vars on the dashboard). Moving this project to a different
GitHub/Supabase/Vercel account later means swapping those values, not
rewriting code. Schema changes are tracked as numbered SQL files in
`schema/` so a new database can be brought up to the same state from
scratch.
