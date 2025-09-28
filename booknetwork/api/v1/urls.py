from django.urls import path, include, re_path

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Apps
    path(
        "ping/",
        include("api.v1.ping.urls"),
    ),
    # Auth
    re_path(
        r"^auth/",
        include("djoser.urls"),
    ),
    # path('auth/', include('djoser.urls.authtoken'),),
    re_path(
        r"^auth/",
        include("djoser.urls.jwt"),
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
