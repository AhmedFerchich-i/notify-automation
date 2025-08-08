
from fastapi import FastAPI

app = FastAPI()

from db.database import Base, engine  # AsyncEngine
from models.email import Email, EmailRecipient, EmailSendStatus, SenderEmail
from models.scheduler import Schedule
from models.user import User

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    print("Creating tables...")
    await create_tables()
    print("Tables created successfully!")

@app.get("/health")
def health_check():
    return {"status": "ok"}

from apis import email

app.include_router(email.router, prefix="/emails", tags=["emails"])