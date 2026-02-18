from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "id",
            "actor_id",
            "action",
            "object_type",
            "object_id",
            "comment_id",
            "created_at",
        ]
