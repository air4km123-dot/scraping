import { getSupabase, ScrapedRow } from "./supabase";

export type FinancialRecord = {
  sourceUrl: string;
  companyName: string | null;
  fiscalYear: string | null;
  revenueThb: string | null;
  netProfitThb: string | null;
  employeeCount: string | null;
  branchCount: string | null;
};

/** Manually-entered data (see scripts/add_financials.py) — grouped by
 * source_url exactly like fetchModuleSnapshot in data.ts, just with
 * financial fields instead of product/price. Shows the latest entry
 * per company regardless of scraped_date, since entries land whenever
 * someone looks the numbers up, not on any daily schedule. */
export async function fetchFinancials(): Promise<FinancialRecord[]> {
  const supabase = getSupabase();

  const { data: rows } = await supabase
    .from("scraped_data")
    .select("source_url, field, value, scraped_at")
    .eq("module", "financials")
    .order("scraped_at", { ascending: true }); // later rows overwrite earlier ones per key below

  const bySource = new Map<string, FinancialRecord>();
  for (const row of (rows ?? []) as Pick<ScrapedRow, "source_url" | "field" | "value">[]) {
    const entry = bySource.get(row.source_url) ?? {
      sourceUrl: row.source_url,
      companyName: null,
      fiscalYear: null,
      revenueThb: null,
      netProfitThb: null,
      employeeCount: null,
      branchCount: null,
    };
    if (row.field === "company_name") entry.companyName = row.value;
    if (row.field === "fiscal_year") entry.fiscalYear = row.value;
    if (row.field === "revenue_thb") entry.revenueThb = row.value;
    if (row.field === "net_profit_thb") entry.netProfitThb = row.value;
    if (row.field === "employee_count") entry.employeeCount = row.value;
    if (row.field === "branch_count") entry.branchCount = row.value;
    bySource.set(row.source_url, entry);
  }

  return Array.from(bySource.values()).sort((a, b) =>
    (a.companyName ?? "").localeCompare(b.companyName ?? "", "th")
  );
}
