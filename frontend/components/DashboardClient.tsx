'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { apiRequest } from '@/lib/api';

type CallItem = {
  id: number;
  file_name: string;
  status: string;
  analysis: {
    scores?: { sentiment_score?: number; buying_intent_score?: number; closing_probability?: number };
    key_moments?: string[];
    executive_summary?: { outcome?: string; call_type?: string };
  };
};

export function DashboardClient() {
  const [calls, setCalls] = useState<CallItem[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    apiRequest('/api/v1/calls', { token })
      .then((data) => setCalls(data as CallItem[]))
      .catch((err: Error) => setError(err.message));
  }, []);

  const metrics = useMemo(() => {
    const analyzed = calls.filter((call) => call.status === 'analyzed');
    const avgSentiment =
      analyzed.reduce((total, call) => total + (call.analysis.scores?.sentiment_score ?? 0), 0) /
      (analyzed.length || 1);
    const avgClose =
      analyzed.reduce((total, call) => total + (call.analysis.scores?.closing_probability ?? 0), 0) /
      (analyzed.length || 1);

    return {
      total: calls.length,
      analyzed: analyzed.length,
      avgSentiment: avgSentiment.toFixed(1),
      avgClose: `${avgClose.toFixed(0)}%`,
    };
  }, [calls]);

  return (
    <div>
      <section className="hero">
        <h2>Revenue command center</h2>
        <p className="muted">
          Inspired by top conversation intelligence products, this dashboard prioritizes key moments,
          conversion signals, and rapid follow-up execution in a minimalist flow.
        </p>
        <div className="kpi-grid">
          <div className="kpi">
            <p className="label">Calls in workspace</p>
            <p className="value">{metrics.total}</p>
          </div>
          <div className="kpi">
            <p className="label">Analyzed calls</p>
            <p className="value">{metrics.analyzed}</p>
          </div>
          <div className="kpi">
            <p className="label">Average sentiment</p>
            <p className="value">{metrics.avgSentiment}/10</p>
          </div>
          <div className="kpi">
            <p className="label">Avg closing probability</p>
            <p className="value">{metrics.avgClose}</p>
          </div>
        </div>
        <p>
          <Link href="/calls">Upload and analyze new calls →</Link>
        </p>
      </section>

      {error && <div className="card">Error loading calls: {error}</div>}

      {calls.map((call) => (
        <article className="card" key={call.id}>
          <h3>{call.file_name}</h3>
          <p className="muted">
            {call.analysis.executive_summary?.call_type ?? 'call'} · {call.analysis.executive_summary?.outcome ?? call.status}
          </p>
          <p>
            Sentiment: {call.analysis.scores?.sentiment_score ?? '-'} · Buying intent:{' '}
            {call.analysis.scores?.buying_intent_score ?? '-'} · Close chance:{' '}
            {call.analysis.scores?.closing_probability ?? '-'}%
          </p>
          <p className="muted">Moments: {call.analysis.key_moments?.join(', ') || 'No flagged moments yet'}</p>
        </article>
      ))}
    </div>
  );
}
