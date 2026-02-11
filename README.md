# SalesOps.ai

SalesOps.ai is a full-stack sales conversation intelligence platform built for modern RevOps teams. It ingests call data, produces structured AI analysis, and helps reps execute high-quality follow-up actions faster.

## Why this project

Sales teams lose momentum when call notes, objections, next steps, and follow-up messaging are spread across disconnected tools. SalesOps.ai consolidates that workflow into one interface:

- **Multi-format intake** (audio/video/transcript files) with queue-based upload.
- **Structured AI analysis** with BANT coverage, sentiment signals, key moments, and close probability.
- **Follow-up acceleration** with generated email draft content and action items.
- **CRM-ready JSON output** designed for downstream Salesforce/HubSpot/PostgreSQL pipelines.

---

## Product UX direction

The UI is intentionally **minimalist and premium** with:

- Dark-first surfaces for analyst-grade readability.
- Warm highlight accents for important actions.
- Blue interaction palette for focus and trust.
- Card-first information hierarchy inspired by modern conversation intelligence dashboards.

---

## Tech Stack

- **Frontend:** Next.js 14 + React 18 + TypeScript (`frontend/`)
- **Backend:** FastAPI + SQLAlchemy async (`backend/`)
- **Database:** SQLite (local default), PostgreSQL-ready schema (`database/`)
- **Infra:** Local and CI scripts (`infrastructure/`)

---

## Local Setup

### 1) Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Create `.env` in repo root (or export vars):

```bash
# Core app
ENV=development
SECRET_KEY=replace-with-a-secure-random-string
DATABASE_URL=sqlite+aiosqlite:///./salesops.db
CORS_ORIGINS=http://localhost:3000
MAX_UPLOAD_MB=500
STORAGE_PATH=./storage

# AI provider keys (for production integrations)
GOOGLE_API_KEY=your_google_ai_studio_key
GEMINI_MODEL_FAST=gemini-2.5-flash
GEMINI_MODEL_DEEP=gemini-2.5-pro
DEEPGRAM_API_KEY=your_deepgram_key
ASSEMBLYAI_API_KEY=your_assemblyai_key
SENDGRID_API_KEY=your_sendgrid_key
```

Run backend:

```bash
uvicorn app.main:app --app-dir backend --reload
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Optional frontend env (`frontend/.env.local`):

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend defaults to `http://localhost:8000`, frontend to `http://localhost:3000`.

---

## Current Feature Coverage

### Call Intake

- Upload transcript/audio/video files.
- Drag-and-drop queue (up to 10 files).
- Validation for file size + format.
- Progress indicators and per-file status.

### Analysis

- Executive call summary.
- Sentiment, buying intent, engagement, and close probability scoring.
- BANT coverage extraction.
- Pain points, objections, key moment detection.
- Follow-up draft scaffolding with drip sequence metadata.

### Dashboard

- KPI tiles for sentiment and close probability.
- Per-call cards for fast triage.
- “Upload and analyze” action flow.

---

## API Overview

- `POST /api/v1/auth/register` — create org + admin user
- `POST /api/v1/auth/login` — issue JWT
- `GET /api/v1/auth/me` — current user profile
- `POST /api/v1/calls/upload` — upload and analyze call
- `GET /api/v1/calls` — list calls in organization
- `GET /api/v1/calls/{id}` — fetch a call

---

## Testing & Quality

From repository root:

```bash
PYTHONPATH=backend pytest backend/tests -q
cd frontend && npm run lint && npm run build
```

---

## Roadmap (high level)

- Google ADK orchestration (Flash vs Pro model routing).
- Real transcription providers with fallback and diarization.
- CRM sync adapters (Salesforce/HubSpot/Pipedrive).
- Advanced analytics dashboards and sentiment heatmaps.
- Human-in-the-loop approvals for outbound messaging.

