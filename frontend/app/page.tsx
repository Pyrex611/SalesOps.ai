import Link from 'next/link';

export default function Home() {
  return (
    <main>
      <section className="hero">
        <h1>SalesOps.ai</h1>
        <p className="muted">
          A sleek conversation intelligence workspace for modern GTM teams. Upload calls, extract strategic
          insights, and launch personalized follow-up workflows in minutes.
        </p>
        <p>
          <Link href="/login">Launch workspace →</Link>
        </p>
      </section>
    </main>
  );
}
