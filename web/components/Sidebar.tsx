"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { href: "/", label: "เปรียบเทียบราคา", hint: "Price Comparison" },
  { href: "/financials", label: "งบกำไรขาดทุน", hint: "Financial Reports" },
  { href: "/news", label: "ข่าวอัพเดท", hint: "Market & News" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <nav className="sidebar" aria-label="Main">
      <div className="sidebar-brand">
        <div className="sidebar-brand-name">Air 4 International</div>
        <div className="sidebar-brand-sub">Competitor Intelligence</div>
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
    </nav>
  );
}
