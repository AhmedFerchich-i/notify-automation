from unittest.mock import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    # SMTP settings (for sending via their own email)
    smtp_server = Column(String(255), nullable=False)
    smtp_port = Column(Integer, nullable=False)
    use_tls = Column(Boolean, default=True)
    smtp_username = Column(String(255), nullable=False)
    smtp_password_encrypted = Column(String, nullable=False)  # Store encrypted!

    is_active = Column(Boolean, default=True)

    # Optional: relationship to emails sent
    email_jobs = relationship("EmailJob", back_populates="user", cascade="all, delete-orphan")
