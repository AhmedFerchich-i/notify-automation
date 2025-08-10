from celery_config.base_config import create_celery_app

celery_app = create_celery_app()

# Add any worker-specific config if needed (usually minimal)
