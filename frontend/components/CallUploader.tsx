'use client';

import { useState } from 'react';
import { apiRequest } from '@/lib/api';

type UploadResponse = {
  analysis: unknown;
};

export function CallUploader() {
  const [status, setStatus] = useState('');
  const [uploading, setUploading] = useState(false);

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

    try {
      setUploading(true);
      const payload = (await apiRequest('/api/v1/calls/upload', {
        method: 'POST',
        token,
        body: form
      })) as UploadResponse;
      setStatus(JSON.stringify(payload.analysis, null, 2));
    } catch (err) {
      setStatus(`Upload failed: ${(err as Error).message}`);
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  return (
    <div className="card">
      <h2>Upload call transcript or recording</h2>
      <input type="file" onChange={onUpload} disabled={uploading} />
      {uploading && <p>Uploading...</p>}
      <pre>{status}</pre>
    </div>
  );
}
