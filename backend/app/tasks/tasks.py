from app.tasks.celery_app import celery_app


@celery_app.task(name="salesops.heartbeat")
def heartbeat() -> dict[str, str]:
    return {"status": "alive"}
