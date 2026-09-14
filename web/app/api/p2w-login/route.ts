import { NextRequest, NextResponse } from "next/server";
import { P2W_COOKIE_NAME, sha256Hex } from "@/lib/p2w-auth";

export async function POST(req: NextRequest) {
  const expected = process.env.P2W_ACCESS_CODE;
  if (!expected) {
    return NextResponse.json(
      { ok: false, error: "P2W_ACCESS_CODE not configured on the server" },
      { status: 500 }
    );
  }

  const body = await req.json().catch(() => null);
  const code = body?.code;
  if (typeof code !== "string" || code !== expected) {
    return NextResponse.json({ ok: false, error: "wrong code" }, { status: 401 });
  }

  const res = NextResponse.json({ ok: true });
  res.cookies.set(P2W_COOKIE_NAME, await sha256Hex(expected), {
    httpOnly: true,
    secure: true,
    sameSite: "lax",
    path: "/p2w",
    maxAge: 60 * 60 * 24 * 30, // 30 days
  });
  return res;
}
