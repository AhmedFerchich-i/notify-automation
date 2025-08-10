from datetime import datetime
from sqlalchemy.orm import Session
from models.email import Email, EmailRecipient, EmailSendStatus, Schedule
from models.email import SendStatusEnum

def schedule_email(
    db: Session,
    subject: str,
    body: str,
    recipients: list[str],
    scheduled_time: datetime | None = None,
) -> Email:
    """
    Creates an Email record with recipients and schedule info.
    If scheduled_time is None, it means send immediately.

    Returns the Email object with all relationships loaded.
    """
    # 1. Create Email instance
    email = Email(
        subject=subject,
        body=body,
        scheduled_time=scheduled_time
    )
    db.add(email)
    db.flush()  # flush so email.id is populated for FK relationships

    # 2. Create EmailRecipient instances
    recipient_objs = []
    for r in recipients:
        recipient = EmailRecipient(email_id=email.id, email_address=r)
        db.add(recipient)
        recipient_objs.append(recipient)

    db.flush()  # flush so recipient IDs are available

    # 3. Create EmailSendStatus for each recipient (status = queued)
    for recipient in recipient_objs:
        status = EmailSendStatus(
            recipient_id=recipient.id,
            status=SendStatusEnum.queued,
            sent_at=None,
            error_message=None,
        )
        db.add(status)

    # 4. If scheduled_time is provided, create Schedule entry
    if scheduled_time is not None:
        schedule = Schedule(
            email_id=email.id,
            scheduled_time=scheduled_time,
            sent=False,
        )
        db.add(schedule)

    db.commit()
    db.refresh(email)
    return email



from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.email import Email  # Assuming Email is your ORM model

def find_due_scheduled_emails(db: Session, lookahead_minutes: int = 1):
    """
    Find emails scheduled to be sent within the given time window.
    Default: find emails scheduled within the next 1 minute.
    """
    now = datetime.utcnow()
    window_end = now + timedelta(minutes=lookahead_minutes)

    return (
        db.query(Email)
        .filter(
            Email.scheduled_at <= window_end,
            Email.sent == False  # Ensure we don’t resend
        )
        .all()
    )
