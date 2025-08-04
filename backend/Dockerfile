FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (optional, add if needed)
# RUN apt-get update && apt-get install -y some-package

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY ./app /app

# Expose FastAPI port
EXPOSE 8000

# Default command runs FastAPI app; overridden in Docker Compose for Celery
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
