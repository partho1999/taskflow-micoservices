from rest_framework import serializers
from .models import Organization, OrganizationMember
from django.utils.text import slugify

def generate_unique_slug(name):
    """
    Generate an auto-unique slug for organization names.
    """
    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    while Organization.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "owner_id",
            "billing_plan",
            "storage_limit_mb",
            "member_limit",
            "auto_join_domain",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner_id", "slug", "created_at", "updated_at"]

    def create(self, validated_data):
        user_id = self.context["user_id"]
        username = self.context["username"]
        validated_data["owner_id"] = user_id

        # Auto-generate UNIQUE slug
        validated_data["slug"] = generate_unique_slug(validated_data["name"])

        org = super().create(validated_data)

        # Create owner membership
        OrganizationMember.objects.create(
            org=org,
            user_id=user_id,
            username=username,
            role=OrganizationMember.ROLE_OWNER,
        )

        return org




class OrganizationMemberSerializer(serializers.ModelSerializer):
    # org_name = serializers.CharField(source="org.name", read_only=True)
    # user_name = serializers.CharField(read_only=True)

    class Meta:
        model = OrganizationMember
        fields = [
            "id",
            "org",
            # "org_name",
            "user_id",
            "username",
            "role",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ChangeMemberRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=OrganizationMember.ROLE_CHOICES
    )