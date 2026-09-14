import TopicNewsPage from "@/components/TopicNewsPage";

export const revalidate = 0;

export default function SolarPage() {
  return (
    <TopicNewsPage
      module="solar_news"
      eyebrow="P2W InterPlus — Internal Intelligence"
      title="โซล่าเซลล์"
      body="ข่าวโซล่าเซลล์ในประเทศไทย โครงการภาครัฐ โครงการสนับสนุนต่างๆ สินค้ารุ่นใหม่ และราคา"
    />
  );
}
