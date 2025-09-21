from django.urls import path

from api.v1.ping import views

urlpatterns = [
    path("", views.PingAPIView.as_view()),
]
