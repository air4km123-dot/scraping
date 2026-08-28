import { getSupabase, ScrapedRow } from "./supabase";

export type Product = {
  sourceUrl: string;
  name: string | null;
  priceThb: string | null;
};

export type ModuleSnapshot = {
  module: string;
  latestDate: string | null;
  products: Product[];
};

const MODULES = ["karshine", "ecoair", "dynamicair", "cooltech"] as const;

/** For one module, find its most recent scrape and group that day's
 * rows by product (source_url) into {name, price}. Every module writes
 * the same (module, source_url, field, value) shape, so this one
 * function works for all of them regardless of what fields a given
 * module happens to publish (e.g. ecoair has no price_thb rows at all). */
async function fetchModuleSnapshot(module: string): Promise<ModuleSnapshot> {
  const supabase = getSupabase();

  const { data: latest } = await supabase
    .from("scraped_data")
    .select("scraped_date")
    .eq("module", module)
    .order("scraped_date", { ascending: false })
    .limit(1)
    .maybeSingle();

  const latestDate = latest?.scraped_date ?? null;
  if (!latestDate) {
    return { module, latestDate: null, products: [] };
  }

  const { data: rows } = await supabase
    .from("scraped_data")
    .select("source_url, field, value")
    .eq("module", module)
    .eq("scraped_date", latestDate);

  const bySource = new Map<string, Product>();
  for (const row of (rows ?? []) as Pick<ScrapedRow, "source_url" | "field" | "value">[]) {
    const entry = bySource.get(row.source_url) ?? {
      sourceUrl: row.source_url,
      name: null,
      priceThb: null,
    };
    if (row.field === "product_name") entry.name = row.value;
    if (row.field === "price_thb") entry.priceThb = row.value;
    bySource.set(row.source_url, entry);
  }

  return {
    module,
    latestDate,
    products: Array.from(bySource.values()).sort((a, b) =>
      (a.name ?? "").localeCompare(b.name ?? "", "th")
    ),
  };
}

export async function fetchAllSnapshots(): Promise<ModuleSnapshot[]> {
  return Promise.all(MODULES.map(fetchModuleSnapshot));
}
