"use client";

import { FormEvent, useState } from "react";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export default function CallsPage() {
  const [status, setStatus] = useState("");
  const [token, setToken] = useState("");

  async function onUpload(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fileInput = (e.currentTarget.elements.namedItem("file") as HTMLInputElement);
    const file = fileInput.files?.[0];
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    const response = await fetch(`${BASE_URL}/calls/upload`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: form,
    });
    setStatus(response.ok ? "Upload accepted and queued for analysis" : "Upload failed");
  }

  return (
    <main>
      <h1>Call Upload</h1>
      <p>Paste API token from login response.</p>
      <input value={token} onChange={(e) => setToken(e.target.value)} placeholder="Bearer token" style={{ width: 380 }} />
      <form onSubmit={onUpload} style={{ marginTop: 12 }}>
        <input type="file" name="file" accept="audio/*,video/mp4" />
        <button type="submit">Upload</button>
      </form>
      <p>{status}</p>
    </main>
  );
}
