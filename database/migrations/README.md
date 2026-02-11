Use Alembic in backend for schema migrations:

1. Set `DATABASE_URL` in backend `.env`.
2. Run `alembic revision --autogenerate -m "your message"`.
3. Run `alembic upgrade head`.
