import P2WSidebar from "@/components/P2WSidebar";

// middleware.ts has already redirected unauthenticated requests to
// /p2w/login before this ever renders, so no auth check needed here.
export default function P2WDashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="shell p2w-shell">
      <P2WSidebar />
      <main className="content">{children}</main>
    </div>
  );
}
