'use client';

import { useState } from 'react';
import { API_BASE } from '@/lib/api';

export function CallUploader() {
  const [status, setStatus] = useState('');

  const onUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }
    const form = new FormData();
    form.append('file', file);
    const res = await fetch(`${API_BASE}/api/v1/calls/upload`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: form
    });
    const payload = await res.json();
    setStatus(JSON.stringify(payload.analysis, null, 2));
  };

  return (
    <div className="card">
      <h2>Upload call transcript or recording</h2>
      <input type="file" onChange={onUpload} />
      <pre>{status}</pre>
    </div>
  );
}
