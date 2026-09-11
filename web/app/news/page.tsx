import { fetchNews } from "@/lib/news";
import ComingSoon from "@/components/ComingSoon";
import NewsCard from "@/components/NewsCard";

export const revalidate = 0;

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

export default async function NewsPage() {
  const { latestDate, items } = await fetchNews();

  if (items.length === 0) {
    return (
      <ComingSoon
        eyebrow="Air 4 International — Competitor Intelligence"
        title="ข่าวอัพเดท"
        body="ข่าวสารและเทรนด์ตลาดทั้งในและต่างประเทศที่อาจกระทบยอดขาย — อัปเดตแบบรายวัน"
        planned={[
          "ยังไม่เคยรัน module ข่าว — รัน `python scripts/run_module.py news` เพื่อดึงข้อมูลครั้งแรก",
        ]}
      />
    );
  }

  return (
    <div className="page">
      <header className="masthead">
        <div className="eyebrow">Air 4 International — Competitor Intelligence</div>
        <h1>ข่าวอัพเดท</h1>
        <p className="sub">
          ข่าวสารและเทรนด์ตลาดที่เกี่ยวกับคู่แข่งทั้ง 10 รายและอุตสาหกรรมล้างแอร์/ล้างหัวฉีดรถยนต์
          จาก Google News และสำนักข่าวไทยโดยตรง
        </p>
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
