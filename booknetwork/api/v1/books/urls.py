from django.urls import path, include
from rest_framework import routers
from api.v1.books import views


router = routers.DefaultRouter()
router.register(
    r"book",
    views.BookViewSet,
)
router.register(
    r"genre",
    views.GenreViewSet,
)
router.register(
    r"author",
    views.AuthurViewSet,
)

urlpatterns = [
    path("", include(router.urls)),
]
