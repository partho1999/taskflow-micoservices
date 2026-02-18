FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# IMPORTANT for JWT RS256
RUN pip install cryptography

COPY . .

EXPOSE 8005

CMD ["gunicorn", "cmt_service.wsgi:application", "--bind", "0.0.0.0:8005"]
