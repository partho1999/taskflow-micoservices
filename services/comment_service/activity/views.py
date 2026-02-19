# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Activity
from .serializers import ActivitySerializer
from .pagination import TraefikAwareCursorPagination

class ActivityListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        actor_id = request.query_params.get("actor_id")
        object_type = request.query_params.get("object_type")

        queryset = Activity.objects.all().order_by("-created_at")
        if actor_id:
            queryset = queryset.filter(actor_id=actor_id)
        if object_type:
            queryset = queryset.filter(object_type=object_type)

        paginator = TraefikAwareCursorPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ActivitySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
