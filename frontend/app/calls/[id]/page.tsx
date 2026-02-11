'use client';

import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { apiRequest } from '@/lib/api';

type CallPayload = {
  id: number;
  file_name: string;
  status: string;
  analysis: {
    executive_summary?: { overview?: string; call_type?: string; outcome?: string };
    scores?: { sentiment_score?: number; buying_intent_score?: number; closing_probability?: number };
    follow_up?: { subject?: string; draft_body?: string; drip_sequence?: Array<{ day: number; message: string }> };
    next_steps?: Array<{ description: string; owner: string }>;
    structured_payload?: { crm_sync?: { status?: string; provider?: string } };
  };
};

export default function CallDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const [call, setCall] = useState<CallPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    try {
      setLoading(true);
      const payload = (await apiRequest(`/api/v1/calls/${id}`, { token })) as CallPayload;
      setCall(payload);
      setError('');
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    load();
  }, [load]);

  const syncToCrm = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      setSyncing(true);
      await apiRequest(`/api/v1/calls/${id}/sync-crm`, { method: 'POST', token });
      await load();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSyncing(false);
    }
  };

  if (loading) {
    return (
      <main>
        <div className="card">Loading call workspace…</div>
      </main>
    );
  }

  if (error) {
    return (
      <main>
        <div className="card error">Error: {error}</div>
      </main>
    );
  }

  if (!call) return null;

  return (
    <main>
      <section className="hero">
        <h1>Post-call workspace</h1>
        <p className="muted">
          Review analysis, send your follow-up draft, and sync details into CRM from a single flow.
        </p>
      </section>

      <section className="card">
        <h2>{call.file_name}</h2>
        <p className="muted">
          {call.analysis.executive_summary?.call_type ?? 'call'} · {call.analysis.executive_summary?.outcome ?? call.status}
        </p>
        <p>{call.analysis.executive_summary?.overview}</p>
      </section>

      <section className="upload-grid">
        <article className="card">
          <h3>Draft follow-up email</h3>
          <p><strong>Subject:</strong> {call.analysis.follow_up?.subject ?? 'N/A'}</p>
          <textarea readOnly value={call.analysis.follow_up?.draft_body ?? 'No draft generated.'} rows={10} />
          <p className="muted">You can copy this draft into your email client or wire it to SendGrid automation.</p>
        </article>

        <article className="card">
          <h3>CRM sync</h3>
          <p>
            Status: {call.analysis.structured_payload?.crm_sync?.status ?? 'pending'}
            {' · '}
            Provider: {call.analysis.structured_payload?.crm_sync?.provider ?? 'not connected'}
          </p>
          <button onClick={syncToCrm} disabled={syncing}>
            {syncing ? 'Syncing…' : 'Sync call to CRM'}
          </button>
          <p className="muted">Managers can customize CRM schema + analysis template in settings.</p>
          <p>
            <Link href="/settings">Open manager settings →</Link>
          </p>
        </article>
      </section>
    </main>
  );
}
