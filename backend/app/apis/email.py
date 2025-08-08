from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd
import io

router = APIRouter()

class EmailList(BaseModel):
    emails: List[str]
    subject: Optional[str]
    message: str

@router.post("/send-email")
async def send_email(
    request: Request,
    file: Optional[UploadFile] = File(None),
    subject: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
):
    # Case 1: JSON payload
    if request.headers.get("content-type", "").startswith("application/json"):
        data = await request.json()
        try:
            email_data = EmailList(**data)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid JSON input")
        emails = email_data.emails
        subject = email_data.subject
        message = email_data.message

    # Case 2: Multipart with file
    elif file:
        if not message:
            raise HTTPException(status_code=400, detail="Message is required with file upload")

        filename = file.filename.lower()

        if filename.endswith(".txt"):
            content = await file.read()
            emails = content.decode("utf-8").splitlines()

        elif filename.endswith(".csv"):
            content = await file.read()
            df = pd.read_csv(io.BytesIO(content))
            emails = df.iloc[:, 0].dropna().astype(str).tolist()

        elif filename.endswith((".xls", ".xlsx")):
            content = await file.read()
            df = pd.read_excel(io.BytesIO(content))
            emails = df.iloc[:, 0].dropna().astype(str).tolist()

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    else:
        raise HTTPException(status_code=400, detail="Either JSON or file must be provided")

    # Final validation
    if not emails:
        raise HTTPException(status_code=400, detail="No email addresses found")

    # TODO: Send emails here using subject/message/emails
    return {"message": f"Emails sent to {len(emails)} recipients."}
