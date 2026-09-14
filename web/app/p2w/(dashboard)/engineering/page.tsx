import TopicNewsPage from "@/components/TopicNewsPage";

export const revalidate = 0;

export default function EngineeringPage() {
  return (
    <TopicNewsPage
      module="engineering_news"
      eyebrow="P2W InterPlus — Internal Intelligence"
      title="วิศวกรรม"
      body="ข่าววงการวิศวกรรมเครื่องกลและด้านอื่นๆ งานที่ปรึกษาด้านวิศวกรรม และงานอบรมเพื่อรับใบเซอร์"
    />
  );
}
