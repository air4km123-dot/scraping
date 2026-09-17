import { fetchAllSnapshots } from "@/lib/data";
import ProductTable from "@/components/ProductTable";

export const revalidate = 0; // always read the latest rows from Supabase, no caching

function formatDate(d: string | null) {
  if (!d) return "no data yet";
  return new Date(d + "T00:00:00Z").toLocaleDateString("th-TH", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export default async function Page() {
  const snapshots = await fetchAllSnapshots();

  return (
    <div className="page">
      <header className="masthead">
        <div className="eyebrow">Air 4 International — Competitor Intelligence</div>
        <h1>เปรียบเทียบราคา</h1>
        <p className="sub">
          Product lineups scraped daily from each competitor&apos;s own website. Where a
          price changed from the previous scrape, it&apos;s marked with{" "}
          <span className="price-arrow up">▲</span> for an increase or{" "}
          <span className="price-arrow down">▼</span> for a decrease. Click a column header
          to sort.
        </p>
      </header>

      <div className="grid">
        {snapshots.map((s) => (
          <section className="card" key={s.module}>
            <h2>{s.module}</h2>
            <div className="meta">
              last updated: {formatDate(s.latestDate)}
              {s.previousDate && <> · vs {formatDate(s.previousDate)}</>}
            </div>
            {s.products.length === 0 ? (
              <p className="empty">No data yet — run this module once.</p>
            ) : (
              <ProductTable products={s.products} />
            )}
          </section>
        ))}
      </div>
    </div>
  );
}
