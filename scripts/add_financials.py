"""
Manual entry tool for competitor financials (งบกำไรขาดทุน).

Why manual: DBD DataWarehouse (datawarehouse.dbd.go.th) — the public
source for Thai company filings — sits behind Imperva/Incapsula bot
protection (verified: every request gets redirect-looped and issued
`visid_incap_*` / `incap_ses_*` challenge cookies). It can't be
scraped on a schedule. A human can still open it in a normal browser,
read the numbers, and key them in here — this just standardizes how
that gets stored, using the same (module, source_url, field, value)
table every scraper module writes to (module="financials").

Real filings come out ~once a year, so this is meant to be run by hand
whenever new numbers are looked up — not on any automated schedule.

Usage:
    python scripts/add_financials.py \\
        --company karshine --name "Karshine" --year 2568 \\
        --revenue 45000000 --profit 3000000 \\
        --employees 25 --branches 3 \\
        --source-url "https://datawarehouse.dbd.go.th/company/profile/5/0105557029574"

Only --company, --name, and --year are required — leave out any
figure you don't have yet (e.g. --employees) and it's simply not
recorded for that year.
"""

import argparse

from storage import get_client  # scripts/ is on sys.path when run directly


def add_financials(
    company: str,
    name: str,
    year: str,
    revenue: str | None,
    profit: str | None,
    employees: str | None,
    branches: str | None,
    source_url: str | None,
) -> int:
    source_url = source_url or f"manual:{company}"
    rows = [{"module": "financials", "source_url": source_url, "field": "company_name", "value": name}]
    rows.append({"module": "financials", "source_url": source_url, "field": "fiscal_year", "value": year})
    if revenue:
        rows.append({"module": "financials", "source_url": source_url, "field": "revenue_thb", "value": revenue})
    if profit:
        rows.append({"module": "financials", "source_url": source_url, "field": "net_profit_thb", "value": profit})
    if employees:
        rows.append({"module": "financials", "source_url": source_url, "field": "employee_count", "value": employees})
    if branches:
        rows.append({"module": "financials", "source_url": source_url, "field": "branch_count", "value": branches})

    client = get_client()
    client.table("scraped_data").upsert(
        rows,
        on_conflict="module,source_url,field,value,scraped_date",
        ignore_duplicates=True,
    ).execute()
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--company", required=True, help="short key, e.g. karshine (matches scrapers/ naming where applicable)")
    parser.add_argument("--name", required=True, help="display name shown on the dashboard, e.g. Karshine")
    parser.add_argument("--year", required=True, help="fiscal year the numbers cover, e.g. 2568")
    parser.add_argument("--revenue", help="annual revenue in THB, digits only")
    parser.add_argument("--profit", help="net profit (or loss, prefix with -) in THB, digits only")
    parser.add_argument("--employees", help="employee count")
    parser.add_argument("--branches", help="branch count")
    parser.add_argument("--source-url", help="DBD profile URL or wherever the numbers came from, for reference")
    args = parser.parse_args()

    n = add_financials(
        args.company, args.name, args.year, args.revenue, args.profit,
        args.employees, args.branches, args.source_url,
    )
    print(f"Recorded {n} fields for {args.name} ({args.year})")
