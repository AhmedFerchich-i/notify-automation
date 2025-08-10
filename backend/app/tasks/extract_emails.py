# tasks/extract.py

from typing import List, Optional, Union
from app.services.email_service import process_email_list
from backend.app.celery_app.celery_worker import celery_app

@celery_app.task
def extract_emails_task(
    message: str,
    file_path: Optional[str] = None,
    email_list: Optional[List[str]] = None,
    subject: Optional[str] = None,
) -> Union[List[str], dict]:
    """
    Celery task to extract email addresses from a file or a direct list and send emails.
    """
    try:
        # Case 1: File input
        if file_path:
            with open(file_path, "rb") as f:
                return process_email_list(file=f, subject=subject, message=message)

        # Case 2: Direct email list
        elif email_list:
            return process_email_list(email_list=email_list, subject=subject, message=message)

        else:
            raise ValueError("You must provide either a file_path or an email_list.")

    except Exception as e:
        # Optional: You can log this error to a file or monitoring tool
        return {"error": str(e)}
