"""
Django settings for cmt_service project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------
# SECURITY
# -----------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DEBUG", "True") in ["1", "True", "true"]
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# -----------------------------------------------------
# INSTALLED APPS
# -----------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "comments",
    "activity",
]

# -----------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Custom JWT middleware
    "cmt_service.middleware.auth_middleware.JWTAuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------------------------------
# CORS
# -----------------------------------------------------
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# -----------------------------------------------------
# URLS & WSGI
# -----------------------------------------------------
ROOT_URLCONF = "cmt_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cmt_service.wsgi.application"

# -----------------------------------------------------
# DATABASE (PostgreSQL)
# -----------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}

# -----------------------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = []

# -----------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------
# STATIC FILES
# -----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------
# JWT CONFIG — RS256 (verify only)
# -----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "cmt_service.core.auth.MicroserviceJWTAuthentication",
    ]
}

# Default key paths
DEFAULT_KEY_PATH = "/app/keys/public.pem"       # Docker path
LOCAL_KEY_PATH = BASE_DIR / "keys/public.pem"  # Local path

JWT_PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH", LOCAL_KEY_PATH)

try:
    with open(JWT_PUBLIC_KEY_PATH, "r") as f:
        JWT_PUBLIC_KEY = f.read()
except FileNotFoundError:
    raise FileNotFoundError(
        f"❌ PUBLIC KEY NOT FOUND!\n"
        f"Tried to load: {JWT_PUBLIC_KEY_PATH}\n"
        f"Make sure the volume /app/keys is correctly mounted."
    )

SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "VERIFYING_KEY": JWT_PUBLIC_KEY,
}

# -----------------------------------------------------
# LOGGING
# -----------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
