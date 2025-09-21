from django.views.generic import TemplateView


class PingTemplateView(TemplateView):
    template_name = "ping.html"
