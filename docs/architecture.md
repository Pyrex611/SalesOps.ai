# Architecture

## Backend
- FastAPI async service exposes REST APIs with JWT auth and RBAC-aware user context.
- SQLAlchemy async models support organizations, users, calls, and call analysis.
- Call pipeline service orchestrates transcription and analysis providers.
- Celery app is included for background and scheduled jobs.

## Frontend
- Next.js 14 App Router UI with pages for login, calls, and dashboard.
- API client wraps backend calls; state uses Zustand.

## Data
- PostgreSQL schema supports multi-tenancy and call intelligence.
- `knowledge_base` table includes `pgvector` column for RAG similarity search.
