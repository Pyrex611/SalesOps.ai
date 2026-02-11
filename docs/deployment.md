# Deployment Guide

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16 (production)
- Redis 7 (for Celery in production)

## Environment Variables

Backend supports:

- `APP_NAME`
- `ENV`
- `SECRET_KEY`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `MAX_UPLOAD_MB`
- `STORAGE_PATH`

Frontend supports:

- `NEXT_PUBLIC_API_URL`

## Production Steps

1. Provision PostgreSQL and Redis.
2. Apply `database/schema.sql` to PostgreSQL.
3. Install backend dependencies and run `uvicorn app.main:app --app-dir backend` behind a process manager.
4. Build frontend with `npm run build` and run `npm run start`.
5. Configure TLS termination and reverse proxy routing.
6. Configure observability (logs, metrics, alerts).
