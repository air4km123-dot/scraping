import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Competitor Intelligence — Air 4 International",
  description: "Daily-refreshed competitor product tracking for Air 4 International.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="th">
      <body>{children}</body>
    </html>
  );
}
