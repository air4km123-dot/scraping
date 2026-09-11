import { fetchAiNews } from "@/lib/ai-news";
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

export default async function AiNewsPage() {
  const { latestDate, items } = await fetchAiNews();

  if (items.length === 0) {
    return (
      <ComingSoon
        eyebrow="Strategic Intelligence — Part 3"
        title="AI อัพเดท"
        body="AI โมเดลใหม่ที่เปิดตัว ความสามารถ และจุดเด่นของแต่ละตัว — อัปเดตแบบรายวัน จาก OpenAI, Google, DeepMind, Hugging Face โดยตรง และ Google News"
        planned={[
          "ยังไม่เคยรัน module นี้ — รัน `python scripts/run_module.py ai_news` เพื่อดึงข้อมูลครั้งแรก",
        ]}
      />
    );
  }

  return (
    <div className="page">
      <header className="masthead">
        <div className="eyebrow">Strategic Intelligence — Part 3</div>
        <h1>AI อัพเดท</h1>
        <p className="sub">
          AI โมเดลใหม่ที่เปิดตัว ความสามารถ และจุดเด่น — จาก OpenAI, Google AI, Gemini,
          DeepMind, Hugging Face โดยตรง และ Google News สำหรับค่ายอื่น (Anthropic, Meta, Mistral, xAI)
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
