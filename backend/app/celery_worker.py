from celery import Celery
from core.settings import settings

celery_app = Celery(
    "notify_automation",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Optional: Configure Celery settings here
celery_app.conf.update(
    task_track_started=True,
    task_time_limit=600,  # seconds, customize as needed
    timezone="UTC",
    enable_utc=True,
)

# Auto-discover tasks from the tasks package
celery_app.autodiscover_tasks(["tasks"])
