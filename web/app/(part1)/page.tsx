import { fetchAllSnapshots, Product } from "@/lib/data";

export const revalidate = 0; // always read the latest rows from Supabase, no caching

function formatDate(d: string | null) {
  if (!d) return "no data yet";
  return new Date(d + "T00:00:00Z").toLocaleDateString("th-TH", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function PriceCell({ product }: { product: Product }) {
  if (!product.priceThb) return <td className="price">—</td>;

  const diff =
    product.priceChange && product.previousPriceThb
      ? Number(product.priceThb) - Number(product.previousPriceThb)
      : null;

  return (
    <td className="price">
      <span className="price-value">{product.priceThb}</span>
      {product.priceChange === "up" && (
        <span className="price-arrow up" title={`เพิ่มขึ้น ${diff} บาท จาก ${product.previousPriceThb}`}>
          ▲ {diff}
        </span>
      )}
      {product.priceChange === "down" && (
        <span className="price-arrow down" title={`ลดลง ${Math.abs(diff ?? 0)} บาท จาก ${product.previousPriceThb}`}>
          ▼ {diff}
        </span>
      )}
    </td>
  );
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
          <span className="price-arrow down">▼</span> for a decrease.
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
                      <PriceCell product={p} />
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
