# scraping — Strategic Data Intelligence Pipeline

Daily-refreshed, multi-module web scraping pipeline. Each topic page runs as
its own scraper module; all modules write into one shared database and feed
one dashboard. Built to run on free-tier infrastructure only.

## Status

- [x] Phase 0 — repo & schema
- [x] Phase 1 — first scraper module (`karshine`, 92 products / 184 rows)
- [x] Phase 2 — storage & dedup (Supabase, verified across reruns)
- [x] Phase 3 — daily automation (GitHub Actions cron, 09:00 Asia/Bangkok, verified live)
- [x] Phase 4 — dashboard v1 (`web/`, Next.js — deployed to Vercel, verified live)
- [x] Phase 5a — `ecoair`, `dynamicair`, `cooltech` added (lineup-only, no published prices)
- [x] Phase 5b — `wise`, `wizard` added (wise has prices via WooCommerce; wizard is lineup-only). 6/10 competitors covered; still open: Freshair, Speedclean, U Cool, NWP — need confirmed target URLs
- [x] Dashboard v2 — sidebar nav (เปรียบเทียบราคา / งบกำไรขาดทุน / ข่าวอัพเดท), day-over-day price arrows (▲ green / ▼ red)
- [x] `news` module — Google News RSS (per-competitor queries) + Thairath/Prachachat RSS (keyword-filtered), daily via GitHub Actions. See ToS caveat below.
- [x] `financials` — manual-entry only (`scripts/add_financials.py`); DBD DataWarehouse blocks automated scraping (Incapsula bot protection, verified). No automated schedule.
- [x] Phase 6 — Telegram alerts. GitHub Actions' 6 modules get one aggregated daily summary (`notify` job); `dynamicair` (runs locally — see below) sends its own message via `scripts/notify_telegram.py`. Any future Part 2 (P2W InterPlus) module that runs locally should call the same helper.

## Known issue: DBD financial data can't be automated

`datawarehouse.dbd.go.th` (the public source for Thai company revenue/
profit/employee/branch filings) sits behind Imperva/Incapsula bot
protection — every request gets redirect-looped with `visid_incap_*`
challenge cookies, confirmed by curl. This can't be scraped on a
schedule. Financials are entered by hand instead, whenever someone
looks the numbers up in a normal browser: `python
scripts/add_financials.py --company <key> --name "<Display Name>"
--year <YYYY> --revenue <THB> --profit <THB> [--employees N]
[--branches N] [--source-url <DBD profile URL>]`. Real filings land
~once a year, so there's no automation to build here — this is just
where the numbers get typed in.

## Known caveat: `news` module and Google News ToS

Google News RSS's own feed text states it's for "personal,
non-commercial use in a feed reader" — used here anyway (per-competitor
search queries), by explicit user decision, alongside Thairath's and
Prachachat's own RSS feeds (ordinary outlet feeds, no such
restriction) as a second, unrestricted source so a story missed by one
still surfaces via the other. Worth revisiting if this ever gets used
outside internal reporting.

## Known issue: `dynamicair` doesn't run on GitHub Actions

`dynamicair.co.th` consistently times out when scraped from GitHub's
runner IP range, but works fine (0.1s connect) from a normal
office/residential connection. It's excluded from the GitHub Actions
matrix and instead runs from a **Windows Task Scheduler task on the
office PC**:

- Task name: `ScrapingDynamicair`
- Schedule: weekdays only (Mon–Fri), 09:00 — same hour as the GitHub
  Actions cron, so every module lines up at one time
- Runs: `C:\Users\BD\run_dynamicair_task.bat` (kept outside the repo, at
  a space-free path, because `schtasks.exe`'s `/tr` argument doesn't
  reliably handle quoted paths containing spaces — it `cd`s into this
  repo, calls `scripts/run_module.py dynamicair`, then
  `scripts/notify_telegram.py dynamicair success|failure` based on the
  exit code)
- Logs to `logs/dynamicair_task.log` (gitignored)
- Needs `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` in the local `.env`
  (same values as the GitHub Actions secrets) for the Telegram step to
  send anything — it just prints a skip message and continues if unset
- **Requires the office PC to be on and online at 09:00** — if it's off,
  asleep, or offline, that day's dynamicair run is silently skipped
  (no automatic catch-up run)

If more competitors turn out to have the same GitHub-IP-blocking issue,
reconsider a paid proxy instead of adding more per-machine scheduled
tasks.

## Dashboard (`web/`)

Next.js app, reads the latest day's rows per module straight from
Supabase server-side (service role key never reaches the browser).

```
cd web
npm install
cp .env.local.example .env.local   # fill in the same 2 values as the root .env
npm run dev
```

To deploy: import this repo on vercel.com (root directory `web/`), add
`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` as Project Environment
Variables (same values as the root `.env` / GitHub Actions secrets).

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
3. Apply every file in `schema/` to your Supabase/Postgres database, in
   numeric order (`001_init.sql`, then `002_scraped_date.sql`, ...).
4. For GitHub Actions to run modules on schedule, add the same values
   from `.env` as repo Secrets (Settings → Secrets and variables →
   Actions): `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, and for
   Telegram alerts `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (create a
   bot via @BotFather, get your chat id from @userinfobot, and message
   your bot once first — Telegram won't let a bot message someone who
   hasn't started a chat with it).
5. Run a module manually: `python scripts/run_module.py karshine`.

## Portability note

No API keys or connection strings are hardcoded anywhere in this repo — they
all come from environment variables (`.env` locally, GitHub Actions Secrets
in CI, Vercel env vars on the dashboard). Moving this project to a different
GitHub/Supabase/Vercel account later means swapping those values, not
rewriting code. Schema changes are tracked as numbered SQL files in
`schema/` so a new database can be brought up to the same state from
scratch.
