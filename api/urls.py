from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserCreateView,
    UserActivityView,
    PostListView,
    PostCreateView,
    PostDetailView,
    PostLikeView,
    PostAnalyticsView,
)

urlpatterns = [
    path("user/signup/", UserCreateView.as_view(), name="user_signup"),
    path("user/activity/<int:pk>/", UserActivityView.as_view(), name="user_activity"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("post/list/", PostListView.as_view(), name="posts"),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
    path("post/update/<int:pk>/", PostDetailView.as_view(), name="post_update"),
    path("post/like/<int:pk>/", PostLikeView.as_view(), name="post_like"),
    path(
        "post/analytics/<int:pk>/", PostAnalyticsView.as_view(), name="post_analytics"
    ),
]
