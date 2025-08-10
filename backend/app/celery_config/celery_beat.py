from celery_config.base_config import create_celery_app

celery_app = create_celery_app()

# Beat-specific config (no redbeat)
celery_app.conf.update(
    beat_scheduler="celery.beat.PersistentScheduler",  # default scheduler
    beat_schedule_filename="celerybeat-schedule",      # stored locally (can persist to volume)
)
