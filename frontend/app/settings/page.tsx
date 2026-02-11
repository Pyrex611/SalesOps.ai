'use client';

import { useEffect, useState } from 'react';
import { apiRequest } from '@/lib/api';

type Templates = {
  crm_field_mapping: Record<string, string>;
  call_analysis_template: Record<string, unknown>;
};

type Me = { role: 'admin' | 'manager' | 'rep' };

export default function SettingsPage() {
  const [role, setRole] = useState<Me['role'] | null>(null);
  const [crmMapping, setCrmMapping] = useState('{\n  "prospect_email": "Contact.Email",\n  "closing_probability": "Opportunity.Close_Probability__c"\n}');
  const [analysisTemplate, setAnalysisTemplate] = useState('{\n  "framework": "BANT",\n  "required_sections": ["executive_summary", "scores", "next_steps"]\n}');
  const [message, setMessage] = useState('');

  const load = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    const me = (await apiRequest('/api/v1/auth/me', { token })) as Me;
    setRole(me.role);

    if (me.role === 'rep') return;

    const templates = (await apiRequest('/api/v1/settings/templates', { token })) as Templates;
    if (Object.keys(templates.crm_field_mapping).length) {
      setCrmMapping(JSON.stringify(templates.crm_field_mapping, null, 2));
    }
    if (Object.keys(templates.call_analysis_template).length) {
      setAnalysisTemplate(JSON.stringify(templates.call_analysis_template, null, 2));
    }
  };

  useEffect(() => {
    load().catch((err: Error) => setMessage(err.message));
  }, []);

  const save = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const payload = {
        crm_field_mapping: JSON.parse(crmMapping),
        call_analysis_template: JSON.parse(analysisTemplate),
      };
      await apiRequest('/api/v1/settings/templates', {
        method: 'PUT',
        token,
        body: JSON.stringify(payload),
      });
      setMessage('Templates saved successfully.');
    } catch (err) {
      setMessage(`Save failed: ${(err as Error).message}`);
    }
  };

  return (
    <main>
      <section className="hero">
        <h1>Manager configuration studio</h1>
        <p className="muted">Create your CRM field format and call analysis format templates for your team.</p>
      </section>

      {role === 'rep' ? (
        <section className="card">
          <p className="error">Only managers/admins can edit templates.</p>
        </section>
      ) : (
        <section className="card">
          <h2>CRM field mapping JSON</h2>
          <textarea value={crmMapping} onChange={(e) => setCrmMapping(e.target.value)} rows={10} />

          <h2>Call analysis template JSON</h2>
          <textarea value={analysisTemplate} onChange={(e) => setAnalysisTemplate(e.target.value)} rows={10} />

          <button onClick={save}>Save templates</button>
          {message && <p className="muted">{message}</p>}
        </section>
      )}
    </main>
  );
}
