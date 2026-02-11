"use client";

import { FormEvent, useState } from "react";

import { apiFetch } from "../../lib/api";
import { useAuthStore } from "../../lib/store";

export default function LoginPage() {
  const [email, setEmail] = useState("rep@example.com");
  const [password, setPassword] = useState("StrongPass123");
  const [message, setMessage] = useState("");
  const setToken = useAuthStore((s) => s.setToken);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    try {
      const data = await apiFetch<{ access_token: string }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setToken(data.access_token);
      setMessage("Login successful. Open dashboard.");
    } catch {
      setMessage("Login failed.");
    }
  }

  return (
    <main>
      <h1>Login</h1>
      <form onSubmit={onSubmit} style={{ display: "grid", maxWidth: 300, gap: 10 }}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        <button type="submit">Login</button>
      </form>
      <p>{message}</p>
    </main>
  );
}
