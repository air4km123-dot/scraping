"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

const NAV_ITEMS = [
  { href: "/p2w/solar", label: "โซล่าเซลล์", hint: "Solar Cell" },
  { href: "/p2w/construction", label: "ก่อสร้าง/รีโนเวท", hint: "Construction" },
  { href: "/p2w/engineering", label: "วิศวกรรม", hint: "Engineering" },
  { href: "/p2w/marketing", label: "ที่ปรึกษาการตลาด", hint: "Marketing" },
  { href: "/p2w/food", label: "วงการอาหาร", hint: "Food Industry" },
  { href: "/p2w/events", label: "อีเว้นกรุงเทพ", hint: "Bangkok Events" },
];

export default function P2WSidebar() {
  const pathname = usePathname();
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/p2w-logout", { method: "POST" });
    router.push("/");
    router.refresh();
  }

  return (
    <nav className="sidebar p2w-sidebar" aria-label="P2W InterPlus">
      <div className="sidebar-brand">
        <div className="sidebar-brand-name">P2W InterPlus</div>
        <div className="sidebar-brand-sub">Internal Intelligence</div>
      </div>
      <ul className="sidebar-nav">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <li key={item.href}>
              <Link href={item.href} className={active ? "active" : ""} aria-current={active ? "page" : undefined}>
                <span className="label">{item.label}</span>
                <span className="hint">{item.hint}</span>
              </Link>
            </li>
          );
        })}
      </ul>
      <button type="button" className="p2w-logout" onClick={handleLogout}>
        ออกจากระบบ
      </button>
    </nav>
  );
}
