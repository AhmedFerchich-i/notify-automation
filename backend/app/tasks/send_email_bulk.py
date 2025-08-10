

from services.email_service import send_bulk_emails
from backend.app.celery_config.celery_worker import celery_app

@celery_app.task
def send_bulk_emails_task(
    smtp_host: str,
    smtp_port: int,
    from_email: str,
    from_password: str,
    subject: str,
    message: str,
    recipients: list[str],
):
    return send_bulk_emails(
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        from_email=from_email,
        from_password=from_password,
        subject=subject,
        message=message,
        recipients=recipients,
    )
