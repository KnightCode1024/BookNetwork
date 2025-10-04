from django.urls import path, include, re_path

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="BookNetwork API",
        default_version="v1",
        description="booknetwork api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Apps
    path(
        "ping/",
        include("api.v1.ping.urls"),
    ),
    path(
        "review/",
        include("api.v1.reviews.urls"),
    ),
    path(
        "book/",
        include("api.v1.books.urls"),
    ),
    # Auth
    re_path(
        r"^auth/",
        include("djoser.urls"),
    ),
    re_path(
        r"^auth/",
        include("djoser.urls.jwt"),
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # DOCS
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
