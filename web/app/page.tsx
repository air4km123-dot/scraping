import { fetchAllSnapshots } from "@/lib/data";

export const revalidate = 0; // always read the latest row from Supabase, no caching

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
        <h1>Direct Competitor Tracker</h1>
        <p className="sub">
          Product lineups scraped daily from each competitor&apos;s own website.
          Prices are shown where the competitor publishes them.
        </p>
      </header>

      <div className="grid">
        {snapshots.map((s) => (
          <section className="card" key={s.module}>
            <h2>{s.module}</h2>
            <div className="meta">last updated: {formatDate(s.latestDate)}</div>
            {s.products.length === 0 ? (
              <p className="empty">No data yet — run this module once.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Price (THB)</th>
                  </tr>
                </thead>
                <tbody>
                  {s.products.map((p) => (
                    <tr key={p.sourceUrl}>
                      <td>
                        <a href={p.sourceUrl} target="_blank" rel="noreferrer">
                          {p.name ?? p.sourceUrl}
                        </a>
                      </td>
                      <td className="price">{p.priceThb ?? "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        ))}
      </div>
    </div>
  );
}
