from django.urls import path
from .views import ActivityListView

app_name = "activity"

urlpatterns = [
    # List all activities
    # GET: /api/activity/?actor_id=<uuid>&object_type=task&page=1&page_size=20
    path("", ActivityListView.as_view(), name="activity-list"),
]
