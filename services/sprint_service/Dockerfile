# -----------------------------
# Base image
# -----------------------------
FROM python:3.12-slim

# -----------------------------
# Set working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Environment variables
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------
# Install dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy application code
# -----------------------------
COPY ./app ./app

# -----------------------------
# Copy keys folder (public.pem) outside app
# -----------------------------
COPY ./keys /keys

# -----------------------------
# Command to run the service
# -----------------------------
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8004"]
