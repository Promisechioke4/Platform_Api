from django.urls import path
from .views import (
    UserListAPIView,
    UserDetailAPIView,
    UserMeAPIView,
    UserRegisterAPIView,
)

urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user_detail"),
    path("users/me/", UserMeAPIView.as_view(), name="user_me"),
    path("register/", UserRegisterAPIView.as_view(), name="user_register"),
]
