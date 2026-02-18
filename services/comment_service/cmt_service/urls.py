"""
URL configuration for cmt_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Comments app
    path("api/comments/", include("comments.urls")),

    # Activity app
    path("api/activity/", include("activity.urls")),
]
