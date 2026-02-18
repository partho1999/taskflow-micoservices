from rest_framework import serializers
from .models import Comment, Mention


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "object_type",
            "object_id",
            "content",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        return Comment.objects.create(
            author_id=user.id,
            **validated_data
        )


class CommentListSerializer(serializers.ModelSerializer):
    mentions = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "object_type",
            "object_id",
            "content",
            "author_id",
            "created_at",
            "updated_at",
            "mentions",
        ]

    def get_mentions(self, obj):
        return [str(m.mentioned_user_id) for m in obj.mentions.all()]


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]
