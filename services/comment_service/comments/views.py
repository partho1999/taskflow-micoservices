import re
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Comment, Mention
from .serializers import (
    CommentCreateSerializer,
    CommentListSerializer,
    CommentUpdateSerializer
)
from activity.models import Activity


class MentionMixin:
    mention_pattern = r"@([0-9a-fA-F-]{36})"

    def extract_mentions(self, content):
        return set(re.findall(self.mention_pattern, content))

    def sync_mentions(self, comment, new_mentions, actor_id):
        existing_mentions = set(
            str(m.mentioned_user_id)
            for m in comment.mentions.all()
        )

        to_add = new_mentions - existing_mentions
        to_remove = existing_mentions - new_mentions

        # Remove old mentions
        if to_remove:
            Mention.objects.filter(
                comment=comment,
                mentioned_user_id__in=to_remove
            ).delete()

        # Add new mentions
        for user_id in to_add:
            Mention.objects.create(
                comment=comment,
                mentioned_user_id=user_id
            )

            Activity.objects.create(
                actor_id=actor_id,
                action="user_mentioned",
                object_type=comment.object_type,
                object_id=comment.object_id,
                comment_id=comment.id,
            )


# ---------------------------
# CREATE COMMENT
# ---------------------------
class CommentCreateView(APIView, MentionMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            comment = serializer.save()

            # Activity: comment created
            Activity.objects.create(
                actor_id=request.user.id,
                action="comment_created",
                object_type=comment.object_type,
                object_id=comment.object_id,
                comment_id=comment.id,
            )

            # Extract mentions
            mentioned_users = self.extract_mentions(comment.content)

            for user_id in mentioned_users:
                Mention.objects.create(
                    comment=comment,
                    mentioned_user_id=user_id
                )

                Activity.objects.create(
                    actor_id=request.user.id,
                    action="user_mentioned",
                    object_type=comment.object_type,
                    object_id=comment.object_id,
                    comment_id=comment.id,
                )

            return Response(
                CommentListSerializer(comment).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# LIST COMMENTS
# ---------------------------
class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        object_type = request.query_params.get("object_type")
        object_id = request.query_params.get("object_id")

        queryset = Comment.objects.filter(is_deleted=False)

        if object_type:
            queryset = queryset.filter(object_type=object_type)

        if object_id:
            queryset = queryset.filter(object_id=object_id)

        queryset = queryset.order_by("-created_at")

        serializer = CommentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------------
# UPDATE COMMENT
# ---------------------------
class CommentUpdateView(APIView, MentionMixin):
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, is_deleted=False)

        if str(comment.author_id) != str(request.user.id):
            return Response(
                {"detail": "You can only edit your own comment."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentUpdateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            updated_comment = serializer.save()

            # Activity: comment updated
            Activity.objects.create(
                actor_id=request.user.id,
                action="comment_updated",
                object_type=updated_comment.object_type,
                object_id=updated_comment.object_id,
                comment_id=updated_comment.id,
            )

            # Sync mentions
            new_mentions = self.extract_mentions(updated_comment.content)
            self.sync_mentions(
                comment=updated_comment,
                new_mentions=new_mentions,
                actor_id=request.user.id
            )

            return Response(CommentListSerializer(updated_comment).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# DELETE COMMENT (Soft Delete)
# ---------------------------
class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, is_deleted=False)

        if str(comment.author_id) != str(request.user.id):
            return Response(
                {"detail": "You can only delete your own comment."},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.is_deleted = True
        comment.save()

        Activity.objects.create(
            actor_id=request.user.id,
            action="comment_deleted",
            object_type=comment.object_type,
            object_id=comment.object_id,
            comment_id=comment.id,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
