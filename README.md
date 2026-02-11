# SalesOps.ai

SalesOps.ai is a full-stack B2B SaaS platform for sales conversation intelligence, with call ingestion, transcript analysis, role-based authentication, and analytics-ready APIs.

## Repository Structure

- `backend/`: FastAPI service, data models, API routes, business logic, and tests.
- `frontend/`: Next.js 14 application with auth flow, dashboard, and call upload screens.
- `database/`: PostgreSQL schema and SQL migrations.
- `infrastructure/`: Local environment scripts and CI setup.
- `docs/`: Architecture and deployment guides.

## Quick Start (Local, no containers)

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Backend URL defaults to `http://localhost:8000` and frontend defaults to `http://localhost:3000`.

## API Overview

- `POST /api/v1/auth/register` create org + admin user
- `POST /api/v1/auth/login` issue JWT
- `GET /api/v1/auth/me` return current user
- `POST /api/v1/calls/upload` upload file and analyze
- `GET /api/v1/calls` list calls in organization
- `GET /api/v1/calls/{id}` fetch a call

## Testing

```bash
PYTHONPATH=backend pytest backend/tests -q
```
