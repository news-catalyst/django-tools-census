from django.views.generic import TemplateView

from responses.conf import settings as app_settings


class Home(TemplateView):
    template_name = "responses/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
