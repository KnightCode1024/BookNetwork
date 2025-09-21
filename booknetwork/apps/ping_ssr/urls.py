from django.urls import path

from apps.ping_ssr import views


urlpatterns = [
    path("", views.PingTemplateView.as_view()),
]
