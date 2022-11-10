from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from . import app_settings
from django.views.generic import TemplateView


class ServiceWorker(TemplateView):
    template_name = app_settings.PWA_SERVICE_WORKER_PATH
    content_type = 'application/javascript'


def manifest(request):
    return render(request, 'manifest.json', {
        setting_name: getattr(app_settings, setting_name)
        for setting_name in dir(app_settings)
        if setting_name.startswith('PWA_')
    }, content_type='application/json')