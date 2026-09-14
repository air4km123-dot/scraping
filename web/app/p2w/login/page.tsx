"use client";

import { useState, FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function P2WLoginPage() {
  const [code, setCode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const res = await fetch("/api/p2w-login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });

    if (res.ok) {
      router.push("/p2w/solar");
      router.refresh();
    } else {
      setLoading(false);
      setError("รหัสผ่านไม่ถูกต้อง");
    }
  }

  return (
    <div className="p2w-login-page">
      <form className="p2w-login-card" onSubmit={handleSubmit}>
        {/* Deliberately unremarkable — anyone who stumbles onto this
            page via the hidden sidebar link should assume it's a
            boring internal tool, not a business portal, and back out. */}
        <div className="p2w-login-brand">ระบบทดสอบ — Error Log Viewer</div>
        <p className="p2w-login-sub">กรอกรหัสผ่านเพื่อดู log</p>
        <input
          type="password"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="รหัสผ่าน"
          autoFocus
          autoComplete="off"
        />
        {error && <p className="p2w-login-error">{error}</p>}
        <div className="p2w-login-actions">
          <Link href="/" className="p2w-login-cancel">
            ยกเลิก
          </Link>
          <button type="submit" disabled={loading || !code}>
            {loading ? "กำลังตรวจสอบ..." : "เข้าสู่ระบบ"}
          </button>
        </div>
      </form>
    </div>
  );
}
