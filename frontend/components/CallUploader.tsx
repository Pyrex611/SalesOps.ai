'use client';

import { useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest } from '@/lib/api';

type UploadResponse = {
  id: number;
  file_name: string;
  status: string;
  analysis: {
    executive_summary?: { overview?: string; call_type?: string; outcome?: string };
    scores?: {
      sentiment_score?: number;
      buying_intent_score?: number;
      closing_probability?: number;
      engagement_score?: number;
    };
    bant?: Record<string, string>;
    pain_points?: string[];
    objections?: string[];
    key_moments?: string[];
    next_steps?: Array<{ description: string; owner: string; status: string }>;
    follow_up?: { subject?: string; draft_body?: string };
  };
};

type UploadItem = {
  file: File;
  progress: number;
  status: 'queued' | 'uploading' | 'analyzed' | 'failed';
  result?: UploadResponse;
  error?: string;
};

const MAX_FILES = 10;
const MAX_BYTES = 500 * 1024 * 1024;
const ACCEPTED = ['.mp3', '.wav', '.m4a', '.mp4', '.webm', '.mov', '.txt'];

export function CallUploader() {
  const router = useRouter();
  const [items, setItems] = useState<UploadItem[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const queueLabel = useMemo(() => `${items.length}/${MAX_FILES} files queued`, [items.length]);

  const validate = (file: File) => {
    const suffix = `.${file.name.split('.').pop()?.toLowerCase() ?? ''}`;
    if (!ACCEPTED.includes(suffix)) {
      return `Unsupported format for ${file.name}.`;
    }
    if (file.size > MAX_BYTES) {
      return `${file.name} exceeds 500MB.`;
    }
    return null;
  };

  const addFiles = (incoming: FileList | null) => {
    if (!incoming?.length) return;
    const nextFiles = Array.from(incoming).slice(0, MAX_FILES - items.length);
    const nextItems: UploadItem[] = [];

    nextFiles.forEach((file) => {
      const invalid = validate(file);
      if (invalid) {
        setError(invalid);
        return;
      }
      nextItems.push({ file, progress: 0, status: 'queued' });
    });

    if (nextItems.length) {
      setError('');
      setItems((current) => [...current, ...nextItems]);
    }
  };

  const updateItem = (index: number, patch: Partial<UploadItem>) => {
    setItems((current) => current.map((item, i) => (i === index ? { ...item, ...patch } : item)));
  };

    }
    return null;
  };

  const addFiles = (incoming: FileList | null) => {
    if (!incoming?.length) return;
    const nextFiles = Array.from(incoming).slice(0, MAX_FILES - items.length);
    const nextItems: UploadItem[] = [];

    nextFiles.forEach((file) => {
      const invalid = validate(file);
      if (invalid) {
        setError(invalid);
        return;
      }
      nextItems.push({ file, progress: 0, status: 'queued' });
    });

    if (nextItems.length) {
      setError('');
      setItems((current) => [...current, ...nextItems]);
    }
  };

  const updateItem = (index: number, patch: Partial<UploadItem>) => {
    setItems((current) => current.map((item, i) => (i === index ? { ...item, ...patch } : item)));
  };

  const analyzeCalls = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }
    if (!items.length) {
      setError('Add at least one file before analyzing.');
      return;
    }

    setUploading(true);
    setError('');

    const completedCallIds: number[] = [];

    for (let i = 0; i < items.length; i += 1) {
      const item = items[i];
      if (item.status === 'analyzed') continue;

      try {
        updateItem(i, { status: 'uploading', progress: 20 });
        const form = new FormData();
        form.append('file', item.file);


    setUploading(true);
    setError('');

    for (let i = 0; i < items.length; i += 1) {
      const item = items[i];
      if (item.status === 'analyzed') continue;

      try {
        updateItem(i, { status: 'uploading', progress: 20 });
        const form = new FormData();
        form.append('file', item.file);

        const simulated = window.setInterval(() => {
          setItems((current) =>
            current.map((currentItem, index) => {
              if (index !== i || currentItem.status !== 'uploading') return currentItem;
              return { ...currentItem, progress: Math.min(currentItem.progress + 12, 90) };
            })
          );
        }, 220);

        const payload = (await apiRequest('/api/v1/calls/upload', {
          method: 'POST',
          token,
          body: form,
        })) as UploadResponse;

        window.clearInterval(simulated);
        updateItem(i, { progress: 100, status: 'analyzed', result: payload });
        completedCallIds.push(payload.id);
      } catch (err) {
        updateItem(i, { status: 'failed', error: (err as Error).message, progress: 100 });
      }
    }

    setUploading(false);

    if (completedCallIds.length > 0) {
      router.push(`/calls/${completedCallIds[0]}`);
      } catch (err) {
        updateItem(i, { status: 'failed', error: (err as Error).message, progress: 100 });
      }
    }

    setUploading(false);
  };

  const resetQueue = () => {
    setItems([]);
    setError('');
  };

  const resetQueue = () => {
    setItems([]);
    setError('');
  };

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Call intake and AI analysis</h2>
        <p>Upload transcripts or recordings, then run analysis when your queue is ready.</p>
      </div>

      <div
        className={`drop-zone ${isDragging ? 'drop-zone--active' : ''}`}
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setIsDragging(false);
          addFiles(event.dataTransfer.files);
        }}
      >
        <p>Drag and drop files here or browse from your device.</p>
        <p className="muted">Supported: MP3, WAV, M4A, MP4, MOV, WebM, TXT · Max 500MB · up to 10 files</p>
        <input
          type="file"
          onChange={(event) => addFiles(event.target.files)}
          disabled={uploading || items.length >= MAX_FILES}
          multiple
        />
      </div>

      <div className="actions-row">
        <span className="badge">{queueLabel}</span>
        <div>
          <button onClick={analyzeCalls} disabled={uploading || !items.length}>
            {uploading ? 'Analyzing queue…' : 'Analyze calls and continue'}
          </button>
          <button className="secondary" onClick={resetQueue} disabled={uploading || !items.length}>
            Reset queue
          </button>
        </div>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="upload-grid">
        {items.map((item, index) => (
          <article className="upload-card" key={`${item.file.name}-${index}`}>
            <div className="upload-card__top">
              <strong>{item.file.name}</strong>
              <span className={`status status--${item.status}`}>{item.status}</span>
            </div>
            <div className="progress">
              <div style={{ width: `${item.progress}%` }} />
            </div>

            {item.error && <p className="error">{item.error}</p>}

            {item.result && (
              <div className="analysis-summary">
                <h3>Analysis snapshot</h3>
                <p>{item.result.analysis.executive_summary?.overview}</p>
                <ul>
                  <li>Sentiment: {item.result.analysis.scores?.sentiment_score ?? '-'}/10</li>
                  <li>Buying intent: {item.result.analysis.scores?.buying_intent_score ?? '-'}/10</li>
                  <li>Closing probability: {item.result.analysis.scores?.closing_probability ?? '-'}%</li>
                  <li>Call type: {item.result.analysis.executive_summary?.call_type ?? '-'}</li>
                </ul>
                <p className="muted">Key moments: {item.result.analysis.key_moments?.join(', ') || 'None detected'}</p>
              </div>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
