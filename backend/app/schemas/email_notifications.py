# schemas/email.py

from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class EmailNotification(BaseModel):
    subject: str
    body: str
    to_addresses: Optional[List[EmailStr]] = None
    send_at: Optional[datetime] = None  # If None, send immediately
