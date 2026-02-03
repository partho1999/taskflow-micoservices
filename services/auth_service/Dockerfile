FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OpenSSL to generate RSA keys
RUN apt-get update && apt-get install -y openssl && apt-get clean

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install cryptography

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000"]
