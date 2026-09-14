import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Competitor Intelligence — Air 4 International",
  description: "Daily-refreshed competitor tracking for Air 4 International.",
};

// Deliberately minimal: Part 1 (Air 4) and Part 2 (P2W InterPlus, behind
// its own login) each define their own shell/sidebar in a nested layout
// so the two never share chrome, navigation, or branding.
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="th">
      <body>{children}</body>
    </html>
  );
}
