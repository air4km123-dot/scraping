import { fetchFinancials } from "@/lib/financials";
import ComingSoon from "@/components/ComingSoon";

export const revalidate = 0;

function formatThb(v: string | null) {
  if (!v) return "—";
  const n = Number(v);
  return Number.isFinite(n) ? n.toLocaleString("th-TH") : v;
}

export default async function FinancialsPage() {
  const records = await fetchFinancials();

  if (records.length === 0) {
    return (
      <ComingSoon
        eyebrow="Air 4 International — Competitor Intelligence"
        title="งบกำไรขาดทุน"
        body="รายได้, กำไร/ขาดทุน, จำนวนพนักงาน และจำนวนสาขาของคู่แข่งแต่ละราย — ข้อมูลนี้บริษัทเอกชนไทยยื่นกับกรมพัฒนาธุรกิจการค้า (DBD) ปีละครั้งเท่านั้น และเว็บ DBD มีระบบป้องกันบอท (Incapsula) จึงดึงอัตโนมัติไม่ได้ ต้องกรอกด้วยมือ"
        planned={[
          "เปิด datawarehouse.dbd.go.th ค้นหาบริษัทคู่แข่งด้วยตัวเอง (ผ่านเบราว์เซอร์ปกติ ไม่ใช่ script)",
          "จดตัวเลข: รายได้, กำไร/ขาดทุนสุทธิ, จำนวนพนักงาน, จำนวนสาขา",
          'บันทึกเข้าระบบด้วยคำสั่ง: python scripts/add_financials.py --company karshine --name "Karshine" --year 2568 --revenue 45000000 --profit 3000000',
        ]}
      />
    );
  }

  return (
    <div className="page">
      <header className="masthead">
        <div className="eyebrow">Air 4 International — Competitor Intelligence</div>
        <h1>งบกำไรขาดทุน</h1>
        <p className="sub">
          ข้อมูลบันทึกด้วยมือจาก DBD DataWarehouse — อัปเดตเมื่อมีการยื่นงบใหม่ (ปีละครั้ง) ไม่ใช่รายวัน
        </p>
      </header>

      <div className="table-wrap">
        <table className="financials-table">
          <thead>
            <tr>
              <th>บริษัท</th>
              <th>ปีงบ</th>
              <th>รายได้ (บาท)</th>
              <th>กำไรสุทธิ (บาท)</th>
              <th>พนักงาน</th>
              <th>สาขา</th>
            </tr>
          </thead>
          <tbody>
            {records.map((r) => (
              <tr key={r.sourceUrl}>
                <td>
                  {r.sourceUrl.startsWith("manual:") ? (
                    r.companyName ?? r.sourceUrl
                  ) : (
                    <a href={r.sourceUrl} target="_blank" rel="noreferrer">
                      {r.companyName ?? r.sourceUrl}
                    </a>
                  )}
                </td>
                <td>{r.fiscalYear ?? "—"}</td>
                <td className="price">{formatThb(r.revenueThb)}</td>
                <td className="price">{formatThb(r.netProfitThb)}</td>
                <td className="price">{r.employeeCount ?? "—"}</td>
                <td className="price">{r.branchCount ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
