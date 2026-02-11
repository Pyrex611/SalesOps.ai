import { CallUploader } from '@/components/CallUploader';

export default function CallsPage() {
  return (
    <main>
      <div className="hero" style={{ marginBottom: '1rem' }}>
        <h1>Call Operations</h1>
        <p className="muted">
          Industry-standard upload workflow with queueing, validation, progress tracking, and one-click analysis.
        </p>
      </div>
      <CallUploader />
    </main>
  );
}
