import { fetchTopicNews } from "@/lib/p2w-news";
import ComingSoon from "@/components/ComingSoon";
import NewsCard from "@/components/NewsCard";

function formatDate(d: string | null) {
  if (!d) return "no data yet";
  return new Date(d + "T00:00:00Z").toLocaleDateString("th-TH", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function formatPublished(raw: string | null) {
  if (!raw) return null;
  const t = Date.parse(raw);
  if (Number.isNaN(t)) return raw;
  return new Date(t).toLocaleDateString("th-TH", { year: "numeric", month: "short", day: "numeric" });
}

/** Shared body for every Part 2 (P2W InterPlus) topic page — all 6
 * modules write the exact same row shape, so this is the one place
 * that renders any of them, parameterized by module name + copy. */
export default async function TopicNewsPage({
  module,
  eyebrow,
  title,
  body,
}: {
  module: string;
  eyebrow: string;
  title: string;
  body: string;
}) {
  const { latestDate, items } = await fetchTopicNews(module);

  if (items.length === 0) {
    return (
      <ComingSoon
        eyebrow={eyebrow}
        title={title}
        body={body}
        planned={[`ยังไม่เคยรัน module นี้ — รัน \`python scripts/run_module.py ${module}\` เพื่อดึงข้อมูลครั้งแรก`]}
      />
    );
  }

  return (
    <div className="page">
      <header className="masthead">
        <div className="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p className="sub">{body}</p>
      </header>

      <div className="meta" style={{ marginBottom: "1.2rem" }}>
        last updated: {formatDate(latestDate)}
      </div>

      <ul className="news-list">
        {items.map((item) => (
          <NewsCard
            key={item.link}
            link={item.link}
            headline={item.headline ?? item.link}
            meta={[item.source, formatPublished(item.publishedAt)].filter((v): v is string => Boolean(v))}
            summary={item.summary}
          />
        ))}
      </ul>
    </div>
  );
}
