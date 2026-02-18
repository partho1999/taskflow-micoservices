from django.urls import path
from .views import (
    CommentCreateView,
    CommentListView,
    CommentUpdateView,
    CommentDeleteView
)

app_name = "comments"

urlpatterns = [
    # ---------------------------
    # Create a new comment
    # POST: /api/comments/
    # ---------------------------
    path("", CommentCreateView.as_view(), name="comment-create"),

    # ---------------------------
    # List all comments
    # GET: /api/comments/list/?object_type=task&object_id=<uuid>
    # ---------------------------
    path("list/", CommentListView.as_view(), name="comment-list"),

    # ---------------------------
    # Update a specific comment by ID
    # PUT: /api/comments/update/<uuid:comment_id>/
    # ---------------------------
    path("update/<uuid:comment_id>/", CommentUpdateView.as_view(), name="comment-update"),

    # ---------------------------
    # Soft delete a specific comment by ID
    # DELETE: /api/comments/delete/<uuid:comment_id>/
    # ---------------------------
    path("delete/<uuid:comment_id>/", CommentDeleteView.as_view(), name="comment-delete"),
]
