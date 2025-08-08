from uuid import uuid4
from sqlalchemy import (
    UUID, Boolean, Column, Integer, String, Text, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime

from db.database import Base

class SendStatusEnum(str, enum.Enum):
    queued = "queued"
    
    sent = "sent"
    bounced = "bounced"
    failed = "failed"

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    scheduled_time = Column(DateTime, nullable=True)  # None means send immediately
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to recipients
    recipients = relationship("EmailRecipient", back_populates="email", cascade="all, delete-orphan")
    schedule = relationship("Schedule", uselist=False, back_populates="email", cascade="all, delete-orphan")

class EmailRecipient(Base):
    __tablename__ = "email_recipients"
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), nullable=False)
    email_address = Column(String(320), nullable=False)  # Max length of an email address
    
    # Relationship back to email
    email = relationship("Email", back_populates="recipients")
    
    # Relationship to send statuses
    send_statuses = relationship("EmailSendStatus", back_populates="recipient", cascade="all, delete-orphan")


class EmailSendStatus(Base):
    __tablename__ = "email_send_statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer, ForeignKey("email_recipients.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(SendStatusEnum), nullable=False, default=SendStatusEnum.queued)
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship back to recipient
    recipient = relationship("EmailRecipient", back_populates="send_statuses")
class SenderEmail(Base):
    __tablename__ = "sender_emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    email = Column(String, nullable=False)  # e.g. "me@gmail.com"
    display_name = Column(String, nullable=True)  # Optional "Ahmed Ferchichi"

    smtp_host = Column(String, nullable=False)  # e.g. smtp.gmail.com
    smtp_port = Column(Integer, nullable=False)  # usually 465 (SSL) or 587 (STARTTLS)
    smtp_username = Column(String, nullable=False)  # often same as email
    smtp_password = Column(String, nullable=False)  # ideally encrypted or stored securely

    use_tls = Column(Boolean, default=True)
    use_ssl = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sender_emails")
