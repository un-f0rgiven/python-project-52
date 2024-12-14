from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils import translation

class DashboardView(TemplateView):
    template_name = 'task_manager/dashboard.html'

    def get(self, request, *args, **kwargs):
        user_language = request.GET.get('language', 'ru')
        translation.activate(user_language)
        request.LANGUAGE_CODE = user_language
        return super().get(request, *args, **kwargs)

class FaviconView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=204)

class IndexView(TemplateView):
    template_name = 'task_manager/index.html'
