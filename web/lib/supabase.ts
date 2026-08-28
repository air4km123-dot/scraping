import { createClient } from "@supabase/supabase-js";

// Server-only client. This file is only ever imported from server
// components (app/page.tsx has no "use client"), so SUPABASE_SERVICE_ROLE_KEY
// never reaches the browser bundle — deliberately not prefixed with
// NEXT_PUBLIC_, which would expose it client-side instead.
export function getSupabase() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    throw new Error(
      "SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set — add them as " +
        "environment variables in Vercel (Project Settings > Environment Variables)."
    );
  }
  return createClient(url, key);
}

export type ScrapedRow = {
  module: string;
  source_url: string;
  field: string;
  value: string | null;
  scraped_at: string;
  scraped_date: string;
};
