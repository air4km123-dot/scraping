// Deliberately has no sidebar/shell of its own — applies to /p2w/login
// (unauthenticated) as well as everything under (dashboard), which
// supplies its own chrome once middleware.ts has let the request through.
export default function P2WLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
