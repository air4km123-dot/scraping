"use client";

import { useState } from "react";

export default function NewsCard({
  link,
  headline,
  meta,
  summary,
}: {
  link: string;
  headline: string;
  meta: string[]; // e.g. [source, publishedDate] — shown as-is, compact
  summary: string | null;
}) {
  const [open, setOpen] = useState(false);

  return (
    <li className="news-item">
      <a href={link} target="_blank" rel="noreferrer">
        {headline}
      </a>
      <div className="news-meta">
        {meta.map((m) => (
          <span key={m}>{m}</span>
        ))}
        {summary && (
          <button
            type="button"
            className="news-summary-toggle"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
          >
            {open ? "ซ่อนสรุป" : "ดูสรุป"}
          </button>
        )}
      </div>
      {open && summary && <p className="news-summary">{summary}</p>}
    </li>
  );
}
