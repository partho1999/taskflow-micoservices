# auth_service/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth API routes
    path("api/auth/", include("users.urls")),
]
