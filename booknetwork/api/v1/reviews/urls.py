from django.urls import path, include
from rest_framework import routers
from api.v1.reviews import views


router = routers.DefaultRouter()
router.register(
    r"",
    views.ReviewViewSet,
)

urlpatterns = [
    path("", include(router.urls)),
]
