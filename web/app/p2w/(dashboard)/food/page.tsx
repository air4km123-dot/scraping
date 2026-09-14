import TopicNewsPage from "@/components/TopicNewsPage";

export const revalidate = 0;

export default function FoodPage() {
  return (
    <TopicNewsPage
      module="food_news"
      eyebrow="P2W InterPlus — Internal Intelligence"
      title="วงการอาหาร"
      body="ข่าววงการอาหาร วัตถุดิบ เนื้อสัตว์ ต้นทุนการผลิต ต้นทุนสินค้า ค่าขนส่ง และแหล่งวัตถุดิบใหม่ๆ"
    />
  );
}
