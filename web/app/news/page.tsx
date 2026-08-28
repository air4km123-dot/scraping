import ComingSoon from "@/components/ComingSoon";

export default function NewsPage() {
  return (
    <ComingSoon
      eyebrow="Air 4 International — Competitor Intelligence"
      title="ข่าวอัพเดท"
      body="ข่าวสารและเทรนด์ตลาดทั้งในและต่างประเทศที่อาจกระทบยอดขาย — อัปเดตแบบรายวัน"
      planned={[
        "Module ดึงข่าวอุตสาหกรรมยานยนต์/เคมีภัณฑ์จากแหล่งข่าวที่เกี่ยวข้อง",
        "ระบบกรองข่าวที่เกี่ยวกับคู่แข่งทั้ง 10 รายโดยเฉพาะ",
        "สรุปผลกระทบต่อธุรกิจแบบย่อต่อข่าวแต่ละชิ้น",
      ]}
    />
  );
}
