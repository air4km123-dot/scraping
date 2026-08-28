import { getSupabase, ScrapedRow } from "./supabase";

export type PriceChange = "up" | "down" | "same" | null;

export type Product = {
  sourceUrl: string;
  name: string | null;
  priceThb: string | null;
  previousPriceThb: string | null;
  priceChange: PriceChange;
};

export type ModuleSnapshot = {
  module: string;
  latestDate: string | null;
  previousDate: string | null;
  products: Product[];
};

const MODULES = ["karshine", "ecoair", "dynamicair", "cooltech", "wise", "wizard"] as const;

type FieldRow = Pick<ScrapedRow, "source_url" | "field" | "value">;

function groupBySource(rows: FieldRow[]): Map<string, { name: string | null; priceThb: string | null }> {
  const bySource = new Map<string, { name: string | null; priceThb: string | null }>();
  for (const row of rows) {
    const entry = bySource.get(row.source_url) ?? { name: null, priceThb: null };
    if (row.field === "product_name") entry.name = row.value;
    if (row.field === "price_thb") entry.priceThb = row.value;
    bySource.set(row.source_url, entry);
  }
  return bySource;
}

/** For one module, find its most recent scrape and the one before it,
 * then group each day's rows by product (source_url) so the latest
 * snapshot can show a price move against the prior one. Every module
 * writes the same (module, source_url, field, value) shape, so this one
 * function works for all of them regardless of what fields a given
 * module happens to publish (e.g. ecoair has no price_thb rows at all
 * — those products just render with no price and no arrow). */
async function fetchModuleSnapshot(module: string): Promise<ModuleSnapshot> {
  const supabase = getSupabase();

  // scraped_date has no long history yet and Supabase's client has no
  // built-in DISTINCT, so pulling every date for the module and
  // deduping here is simplest at this data volume.
  const { data: dateRows } = await supabase
    .from("scraped_data")
    .select("scraped_date")
    .eq("module", module)
    .order("scraped_date", { ascending: false });

  const distinctDates = Array.from(new Set((dateRows ?? []).map((r) => r.scraped_date)));
  const [latestDate, previousDate] = [distinctDates[0] ?? null, distinctDates[1] ?? null];

  if (!latestDate) {
    return { module, latestDate: null, previousDate: null, products: [] };
  }

  const { data: latestRows } = await supabase
    .from("scraped_data")
    .select("source_url, field, value")
    .eq("module", module)
    .eq("scraped_date", latestDate);

  const latestBySource = groupBySource((latestRows ?? []) as FieldRow[]);

  let previousBySource = new Map<string, { name: string | null; priceThb: string | null }>();
  if (previousDate) {
    const { data: previousRows } = await supabase
      .from("scraped_data")
      .select("source_url, field, value")
      .eq("module", module)
      .eq("scraped_date", previousDate);
    previousBySource = groupBySource((previousRows ?? []) as FieldRow[]);
  }

  const products: Product[] = Array.from(latestBySource.entries()).map(([sourceUrl, latest]) => {
    const previous = previousBySource.get(sourceUrl);
    const previousPriceThb = previous?.priceThb ?? null;

    let priceChange: PriceChange = null;
    if (latest.priceThb && previousPriceThb) {
      const latestNum = Number(latest.priceThb);
      const previousNum = Number(previousPriceThb);
      if (Number.isFinite(latestNum) && Number.isFinite(previousNum)) {
        priceChange = latestNum > previousNum ? "up" : latestNum < previousNum ? "down" : "same";
      }
    }

    return {
      sourceUrl,
      name: latest.name,
      priceThb: latest.priceThb,
      previousPriceThb,
      priceChange,
    };
  });

  products.sort((a, b) => (a.name ?? "").localeCompare(b.name ?? "", "th"));

  return { module, latestDate, previousDate, products };
}

export async function fetchAllSnapshots(): Promise<ModuleSnapshot[]> {
  return Promise.all(MODULES.map(fetchModuleSnapshot));
}
