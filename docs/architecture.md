# Architecture Overview

## Backend

FastAPI provides async HTTP APIs, JWT auth, role-aware access boundaries, and organizational multi-tenancy.

- API Layer: `backend/app/api/v1`
- Service Layer: `backend/app/services`
- Data Layer: SQLAlchemy async models and sessions
- Worker Layer: Celery app for asynchronous jobs

## Frontend

Next.js App Router provides login/register, dashboard visualization, and upload workflow.

- Login flow stores JWT token in browser local storage
- Dashboard fetches call analytics from backend APIs
- Calls page uploads files as multipart form data

## Data Model

Core tables:

- `organizations`
- `users`
- `calls`

Schema source of truth: `database/schema.sql`.

## Security Model

- Password hashing with bcrypt via Passlib
- JWT token authentication
- CORS allowlist configuration
- Organization-scoped call access checks

## Extensibility

- Replace local transcript adapter with Deepgram adapter in `TranscriptionService`
- Replace heuristic analysis engine with Gemini adapter in `AnalysisService`
- Extend models for CRM sync, RAG knowledge base, and advanced reporting
