export default function ComingSoon({
  eyebrow,
  title,
  body,
  planned,
}: {
  eyebrow: string;
  title: string;
  body: string;
  planned: string[];
}) {
  return (
    <div className="page">
      <header className="masthead">
        <div className="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p className="sub">{body}</p>
      </header>

      <section className="card coming-soon">
        <div className="badge">ยังไม่เปิดใช้งาน</div>
        <p>ส่วนนี้ยังไม่มีข้อมูล — ต้องสร้างตัวดึงข้อมูลเพิ่มเติมก่อน:</p>
        <ul>
          {planned.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
