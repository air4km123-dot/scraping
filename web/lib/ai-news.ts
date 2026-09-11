import { getSupabase, ScrapedRow } from "./supabase";

export type AiNewsItem = {
  link: string;
  headline: string | null;
  source: string | null;
  publishedAt: string | null;
  summary: string | null;
};

export type AiNewsSnapshot = {
  latestDate: string | null;
  items: AiNewsItem[];
};

/** Same "group by source_url, latest scraped_date" shape as
 * lib/news.ts, with an added summary field (the model/feature
 * capability blurb the user specifically asked to see). */
export async function fetchAiNews(): Promise<AiNewsSnapshot> {
  const supabase = getSupabase();

  const { data: latest } = await supabase
    .from("scraped_data")
    .select("scraped_date")
    .eq("module", "ai_news")
    .order("scraped_date", { ascending: false })
    .limit(1)
    .maybeSingle();

  const latestDate = latest?.scraped_date ?? null;
  if (!latestDate) return { latestDate: null, items: [] };

  const { data: rows } = await supabase
    .from("scraped_data")
    .select("source_url, field, value")
    .eq("module", "ai_news")
    .eq("scraped_date", latestDate);

  const byLink = new Map<string, AiNewsItem>();
  for (const row of (rows ?? []) as Pick<ScrapedRow, "source_url" | "field" | "value">[]) {
    const entry = byLink.get(row.source_url) ?? {
      link: row.source_url,
      headline: null,
      source: null,
      publishedAt: null,
      summary: null,
    };
    if (row.field === "headline") entry.headline = row.value;
    if (row.field === "source") entry.source = row.value;
    if (row.field === "published_at") entry.publishedAt = row.value;
    if (row.field === "summary") entry.summary = row.value;
    byLink.set(row.source_url, entry);
  }

  const items = Array.from(byLink.values()).sort((a, b) => {
    const at = a.publishedAt ? Date.parse(a.publishedAt) : 0;
    const bt = b.publishedAt ? Date.parse(b.publishedAt) : 0;
    return bt - at;
  });

  return { latestDate, items };
}
