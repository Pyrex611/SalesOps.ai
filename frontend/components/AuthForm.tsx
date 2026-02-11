'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiRequest } from '@/lib/api';

export function AuthForm() {
  const router = useRouter();
  const [mode, setMode] = useState<'login' | 'register'>('register');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [org, setOrg] = useState('');
  const [error, setError] = useState('');

  const submit = async () => {
    try {
      setError('');
      if (mode === 'register') {
        await apiRequest('/api/v1/auth/register', {
          method: 'POST',
          body: JSON.stringify({
            organization_name: org,
            full_name: name,
            email,
            password
          })
        });
      }
      const token = await apiRequest('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });
      localStorage.setItem('token', token.access_token);
      router.push('/dashboard');
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <div className="card">
      <h2>{mode === 'register' ? 'Create account' : 'Sign in'}</h2>
      {mode === 'register' && (
        <>
          <label>Organization</label>
          <input value={org} onChange={(e) => setOrg(e.target.value)} />
          <label>Full name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} />
        </>
      )}
      <label>Email</label>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <label>Password</label>
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={submit}>{mode === 'register' ? 'Register + Login' : 'Login'}</button>
      <button onClick={() => setMode(mode === 'register' ? 'login' : 'register')}>
        Switch to {mode === 'register' ? 'login' : 'register'}
      </button>
      {error && <p>{error}</p>}
    </div>
  );
}
