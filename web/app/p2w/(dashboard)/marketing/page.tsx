import TopicNewsPage from "@/components/TopicNewsPage";

export const revalidate = 0;

export default function MarketingPage() {
  return (
    <TopicNewsPage
      module="marketing_news"
      eyebrow="P2W InterPlus — Internal Intelligence"
      title="ที่ปรึกษาการตลาด"
      body="ข่าววงการที่ปรึกษาการตลาด แนวโน้ม การอบรม งานอีเว้นในกรุงเทพฯ"
    />
  );
}
