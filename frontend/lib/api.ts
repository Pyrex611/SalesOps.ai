const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

type ApiRequestOptions = RequestInit & {
  token?: string | null;
};

export async function apiRequest(path: string, options: ApiRequestOptions = {}) {
  const { token, headers, body, ...rest } = options;
  const requestHeaders = new Headers(headers || undefined);

  if (token) {
    requestHeaders.set('Authorization', `Bearer ${token}`);
  }

  if (body && !(body instanceof FormData) && !requestHeaders.has('Content-Type')) {
    requestHeaders.set('Content-Type', 'application/json');
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...rest,
    body,
    headers: requestHeaders,
    cache: 'no-store'
  });

  const contentType = res.headers.get('content-type') ?? '';
  const isJson = contentType.includes('application/json');
  const payload = isJson ? await res.json() : await res.text();

  if (!res.ok) {
    const message =
      typeof payload === 'object' && payload !== null && 'detail' in payload
        ? String((payload as { detail: string }).detail)
        : String(payload || 'Request failed');
    throw new Error(message);
  }

  return payload;
}

export { API_BASE };
