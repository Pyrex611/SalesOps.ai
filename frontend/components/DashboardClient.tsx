'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { API_BASE } from '@/lib/api';

type CallItem = {
  id: number;
  file_name: string;
  status: string;
  analysis: { sentiment_score?: number; buying_intent_score?: number };
};

export function DashboardClient() {
  const [calls, setCalls] = useState<CallItem[]>([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }
    fetch(`${API_BASE}/api/v1/calls`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: 'no-store'
    })
      .then((r) => r.json())
      .then((data) => setCalls(data));
  }, []);

  return (
    <div>
      <div className="card">
        <h2>Quick Actions</h2>
        <Link href="/calls">Upload and analyze call</Link>
      </div>
      {calls.map((call) => (
        <div className="card" key={call.id}>
          <h3>{call.file_name}</h3>
          <p>Status: {call.status}</p>
          <p>Sentiment: {call.analysis.sentiment_score ?? '-'}</p>
          <p>Buying Intent: {call.analysis.buying_intent_score ?? '-'}</p>
        </div>
      ))}
    </div>
  );
}
