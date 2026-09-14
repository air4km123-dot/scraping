// Shared by the login API route (Node runtime) and middleware.ts (Edge
// runtime) — Web Crypto's subtle.digest works in both, so this file
// works unmodified in either.

export const P2W_COOKIE_NAME = "p2w_session";

export async function sha256Hex(text: string): Promise<string> {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

/** The cookie never holds the access code itself — just a hash of it,
 * so the code isn't sitting in plaintext in the browser or in transit
 * after the initial login POST. */
export async function expectedCookieValue(): Promise<string | null> {
  const code = process.env.P2W_ACCESS_CODE;
  if (!code) return null;
  return sha256Hex(code);
}
