# users/urls.py
from django.urls import path
from .views import SignupView, LoginView, RefreshTokenView, UserListView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("users/", UserListView.as_view(), name="user-list"),
]