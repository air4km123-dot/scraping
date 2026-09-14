import TopicNewsPage from "@/components/TopicNewsPage";

export const revalidate = 0;

export default function EventsPage() {
  return (
    <TopicNewsPage
      module="bangkok_events"
      eyebrow="P2W InterPlus — Internal Intelligence"
      title="อีเว้นกรุงเทพ"
      body="อีเว้นและกิจกรรมในกรุงเทพฯ และจังหวัดใกล้เคียงที่กำลังจะเกิดขึ้น หรือเปิดรับสมัคร"
    />
  );
}
