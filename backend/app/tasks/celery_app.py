from celery import Celery

celery_app = Celery("salesops", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")
celery_app.conf.task_always_eager = False
