from db.database import Base, engine
from models.email import Email,EmailRecipient,EmailSendStatus,SenderEmail
from models.scheduler import Schedule
from models.user import User

# Create all tables in the database
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")