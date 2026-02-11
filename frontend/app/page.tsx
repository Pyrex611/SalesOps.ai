import Link from "next/link";

export default function HomePage() {
  return (
    <main>
      <h1>SalesOps.ai</h1>
      <p>Enterprise AI conversation intelligence platform.</p>
      <ul>
        <li><Link href="/login">Login</Link></li>
        <li><Link href="/dashboard">Dashboard</Link></li>
        <li><Link href="/calls">Calls</Link></li>
      </ul>
    </main>
  );
}
