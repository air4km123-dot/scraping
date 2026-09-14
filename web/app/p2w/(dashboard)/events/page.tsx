import TopicNewsPage from "@/components/TopicNewsPage";

export const revalidate = 0;

export default function EventsPage() {
  return (
    <TopicNewsPage
      module="central_events"
      eyebrow="P2W InterPlus — Internal Intelligence"
      title="อีเว้นภาคกลาง"
      body="อีเว้นและกิจกรรมในกรุงเทพฯ และภาคกลางที่กำลังจะเกิดขึ้น หรือเปิดรับสมัคร"
    />
  );
}
