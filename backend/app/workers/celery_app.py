from celery import Celery

celery_app = Celery('salesops', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
celery_app.conf.update(task_serializer='json', result_serializer='json', timezone='UTC')


@celery_app.task(name='health.ping')
def ping() -> str:
    return 'pong'
