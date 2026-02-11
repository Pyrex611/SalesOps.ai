# SalesOps.ai Platform

Production-ready baseline for an AI-powered sales call intelligence platform.

## Monorepo Layout

- `backend/`: FastAPI API, auth, call ingestion, transcription + analysis pipeline, Celery tasks, tests.
- `frontend/`: Next.js 14 app with login, dashboard, and call upload flows.
- `database/`: PostgreSQL schema and migration notes.
- `docs/`: architecture, API, deployment, and operations docs.

## Local Development (No Containers)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Overview

- `POST /api/v1/organizations`
- `POST /api/v1/users`
- `POST /api/v1/auth/login`
- `POST /api/v1/calls/upload`
- `GET /api/v1/calls`
- `GET /api/v1/calls/{id}/analysis`

## Testing

```bash
cd backend
pytest -q
```
