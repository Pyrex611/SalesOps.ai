import Link from 'next/link';

export default function Home() {
  return (
    <main>
      <h1>SalesOps.ai</h1>
      <p>Conversation intelligence and sales automation platform.</p>
      <Link href="/login">Get started</Link>
    </main>
  );
}
