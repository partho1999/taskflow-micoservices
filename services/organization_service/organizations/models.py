import uuid
from django.db import models


class Organization(models.Model):
    """
    Premium Jira-like Organization Model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Main fields
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    owner_id = models.UUIDField()  # UUID from auth_service

    # Billing
    BILLING_FREE = "free"
    BILLING_PRO = "pro"

    BILLING_CHOICES = [
        (BILLING_FREE, "Free"),
        (BILLING_PRO, "Pro"),
    ]

    billing_plan = models.CharField(
        max_length=20, choices=BILLING_CHOICES, default=BILLING_FREE
    )
    storage_limit_mb = models.IntegerField(default=500)  # free default
    member_limit = models.IntegerField(default=5)  # free default

    # Domain-based auto join (like Google Workspace)
    auto_join_domain = models.CharField(max_length=150, blank=True)

    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrganizationMember(models.Model):
    """
    Members table like Jira Groups
    """

    ROLE_OWNER = "owner"
    ROLE_ADMIN = "admin"
    ROLE_MEMBER = "member"

    ROLE_CHOICES = [
        (ROLE_OWNER, "Owner"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_MEMBER, "Member"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    user_id = models.UUIDField()  # UUID from auth_service
    username = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("org", "user_id")

    def __str__(self):
        return f"{self.user_id} @ {self.org.name}"


class OrganizationInvite(models.Model):
    """
    Email invitation system
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="invites")
    email = models.EmailField()
    invited_by_id = models.UUIDField()  # user UUID
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    # Status
    is_accepted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("org", "email")

    def __str__(self):
        return f"Invite {self.email} -> {self.org.name}"
