from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "full_name", "bio", "avatar",
            "timezone", "language", "organization_id", "password"
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users.
    Only returns username.
    """
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
        ]
