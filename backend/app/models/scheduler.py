from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from db.database import Base

class Schedule(Base):
    __tablename__ = "email_schedules"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    scheduled_time = Column(DateTime, nullable=False)
    sent = Column(Boolean, default=False, nullable=False)  # Explicitly not nullable

    email = relationship("Email", back_populates="schedule")
