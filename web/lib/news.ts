import { getSupabase, ScrapedRow } from "./supabase";

export type NewsItem = {
  link: string;
  headline: string | null;
  source: string | null;
  publishedAt: string | null;
};

export type NewsSnapshot = {
  latestDate: string | null;
  items: NewsItem[];
};

/** Same "group by source_url, latest scraped_date" shape as
 * fetchModuleSnapshot in data.ts, just with news-specific fields
 * (headline/source/published_at) instead of product/price. */
export async function fetchNews(): Promise<NewsSnapshot> {
  const supabase = getSupabase();

  const { data: latest } = await supabase
    .from("scraped_data")
    .select("scraped_date")
    .eq("module", "news")
    .order("scraped_date", { ascending: false })
    .limit(1)
    .maybeSingle();

  const latestDate = latest?.scraped_date ?? null;
  if (!latestDate) return { latestDate: null, items: [] };

  const { data: rows } = await supabase
    .from("scraped_data")
    .select("source_url, field, value")
    .eq("module", "news")
    .eq("scraped_date", latestDate);

  const byLink = new Map<string, NewsItem>();
  for (const row of (rows ?? []) as Pick<ScrapedRow, "source_url" | "field" | "value">[]) {
    const entry = byLink.get(row.source_url) ?? {
      link: row.source_url,
      headline: null,
      source: null,
      publishedAt: null,
    };
    if (row.field === "headline") entry.headline = row.value;
    if (row.field === "source") entry.source = row.value;
    if (row.field === "published_at") entry.publishedAt = row.value;
    byLink.set(row.source_url, entry);
  }

  const items = Array.from(byLink.values()).sort((a, b) => {
    const at = a.publishedAt ? Date.parse(a.publishedAt) : 0;
    const bt = b.publishedAt ? Date.parse(b.publishedAt) : 0;
    return bt - at;
  });

  return { latestDate, items };
}
