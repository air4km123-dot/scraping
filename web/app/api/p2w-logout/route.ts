import { NextResponse } from "next/server";
import { P2W_COOKIE_NAME } from "@/lib/p2w-auth";

export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set(P2W_COOKIE_NAME, "", { path: "/p2w", maxAge: 0 });
  return res;
}
