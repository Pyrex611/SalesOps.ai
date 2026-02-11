# Deployment (Non-containerized)

## Requirements
- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- Redis 7

## Backend
1. Install dependencies and set `.env` with production secrets.
2. Run migrations with Alembic.
3. Start API: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
4. Start worker: `celery -A app.tasks.celery_app.celery_app worker -l info`.

## Frontend
1. Build app: `npm run build`.
2. Start app: `npm run start`.
3. Set `NEXT_PUBLIC_API_URL` to API base URL.
