import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_path(instance, filename):
    return f"avatars/{instance.id}/{filename}"


class User(AbstractUser):
    """
    Custom User Model for TaskFlow (Jira-like)
    Ready for microservices & scalable.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # override email field to make it unique
    email = models.EmailField(unique=True)

    # Basic profile
    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    # User preferences
    timezone = models.CharField(max_length=50, default="UTC")
    language = models.CharField(max_length=10, default="en")

    is_email_verified = models.BooleanField(default=False)

    organization_id = models.UUIDField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
