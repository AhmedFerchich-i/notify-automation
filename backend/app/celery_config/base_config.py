from celery import Celery
from core.settings import settings

def create_celery_app():
    app = Celery(
        "notify_automation",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )
    app.conf.update(
        task_track_started=True,
        task_time_limit=600,
        timezone="UTC",
        enable_utc=True,
    )
    app.autodiscover_tasks(["tasks"])
    return app
