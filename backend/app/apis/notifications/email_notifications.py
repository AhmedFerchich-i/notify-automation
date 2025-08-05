from fastapi import APIRouter, UploadFile, File, Form, HTTPException

import io
import csv
import pandas as pd
from schemas.email_notifications import EmailNotification
router=APIRouter()

@router.post("/send-email-to-list")
async def send_email_to_list(note:EmailNotification):
    pass


@router.post("/send-email-to-txt")
async def send_email_to_txt(subject: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(...)):
    pass

@router.post("/send-email-to-csv")
async def send_email_to_csv(subject: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(...)):
    pass

@router.post("/send-email-to-excel")
async def send_email_to_excel(subject: str = Form(...),
    message: str = Form(...),
    file: UploadFile = File(...)):
    pass