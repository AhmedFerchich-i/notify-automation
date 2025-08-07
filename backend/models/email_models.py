from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime

Base = declarative_base()

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
