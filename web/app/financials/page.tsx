import ComingSoon from "@/components/ComingSoon";

export default function FinancialsPage() {
  return (
    <ComingSoon
      eyebrow="Air 4 International — Competitor Intelligence"
      title="งบกำไรขาดทุน"
      body="รายได้, กำไร/ขาดทุน, จำนวนพนักงาน และจำนวนสาขาของคู่แข่งแต่ละราย — ข้อมูลนี้บริษัทเอกชนไทยยื่นกับกรมพัฒนาธุรกิจการค้า (DBD) ปีละครั้งเท่านั้น จึงอัปเดตแบบรายเดือน/รายไตรมาส ไม่ใช่รายวัน"
      planned={[
        "Module ดึงข้อมูลงบการเงินจาก DBD Datawarehouse ต่อคู่แข่งแต่ละราย",
        "ตารางเทียบรายได้/กำไรย้อนหลังหลายปี",
        "กราฟแนวโน้มจำนวนพนักงานและจำนวนสาขา",
      ]}
    />
  );
}
