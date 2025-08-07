import smtplib
from email.mime.text import MIMEText
from core.settings import settings
from typing import Any, List
from adapters.email_list_adapter import JsonListEmailAdapter

from utils.email_utils import send_email

from fastapi import UploadFile
from typing import Dict
from adapters.email_list_adapter import (
    CsvFileEmailAdapter,
    TxtFileEmailAdapter,
    ExcelFileEmailAdapter,
)




def send_bulk_emails(
    smtp_host: str,
    smtp_port: int,
    from_email: str,
    from_password: str,
    subject: str,
    message: str,
    recipients: List[str]
) -> Dict[str, List[str]]:
    """
    Send emails in bulk and return success/failure info.

    Returns:
        {
            "success": [list of emails sent successfully],
            "failed": [list of failed emails with error messages]
        }
    """
    success = []
    failed = []

    for to_email in recipients:
        try:
            send_email(
                smtp_host=smtp_host,
                smtp_port=smtp_port,
                from_email=from_email,
                from_password=from_password,
                to_email=to_email,
                subject=subject,
                message=message
            )
            success.append(to_email)
        except Exception as e:
            failed.append(f"{to_email}: {str(e)}")

    return {
        "success": success,
        "failed": failed
    }

# Map file types to their corresponding adapter
ADAPTER_MAP: Dict[str, object] = {
    "csv": CsvFileEmailAdapter(),
    "txt": TxtFileEmailAdapter(),
    "xlsx": ExcelFileEmailAdapter(),
    "xls": ExcelFileEmailAdapter(),
    "list": JsonListEmailAdapter(),  # <-- NEW
}

def process_email_list(
    file: UploadFile = None,
    email_list: List[str] = None,
    subject: str = None,
    message: str = None,
) -> List[str]:
    if file:
        file_type = file.filename.split(".")[-1].lower()
        adapter = ADAPTER_MAP.get(file_type)

        if not adapter:
            raise ValueError(f"Unsupported file type: {file_type}")

        content = file.file.read()
        return adapter.get_emails(content)

    elif email_list:
        adapter = ADAPTER_MAP.get("json_list")
        return adapter.get_emails(email_list)

    else:
        raise ValueError("Either file or email_list must be provided.")
