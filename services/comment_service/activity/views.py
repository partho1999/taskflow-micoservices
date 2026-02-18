from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Activity
from .serializers import ActivitySerializer


# ---------------------------
# Pagination Class
# ---------------------------
class ActivityPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


# ---------------------------
# List Activities
# ---------------------------
class ActivityListView(ListAPIView):
    """
    List activities with optional filtering by actor_id, object_type, or comment_id.
    Paginated by default.
    """
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ActivityPagination

    def get_queryset(self):
        queryset = Activity.objects.all().order_by("-created_at")
        actor_id = self.request.query_params.get("actor_id")
        object_type = self.request.query_params.get("object_type")
        comment_id = self.request.query_params.get("comment_id")

        if actor_id:
            queryset = queryset.filter(actor_id=actor_id)
        if object_type:
            queryset = queryset.filter(object_type=object_type)
        if comment_id:
            queryset = queryset.filter(comment_id=comment_id)

        return queryset
