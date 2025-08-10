from celery_app.base_config import create_celery_app

celery_app = create_celery_app()

# Add any worker-specific config if needed (usually minimal)
