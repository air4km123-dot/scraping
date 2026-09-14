import { NextRequest, NextResponse } from "next/server";
import { P2W_COOKIE_NAME, expectedCookieValue } from "@/lib/p2w-auth";

export const config = {
  matcher: ["/p2w/:path*"],
};

export async function middleware(req: NextRequest) {
  if (req.nextUrl.pathname === "/p2w/login") {
    return NextResponse.next();
  }

  const cookie = req.cookies.get(P2W_COOKIE_NAME)?.value;
  const expected = await expectedCookieValue();

  if (!expected || cookie !== expected) {
    return NextResponse.redirect(new URL("/p2w/login", req.url));
  }
  return NextResponse.next();
}
