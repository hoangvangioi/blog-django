from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import manifest, ServiceWorker


# Serve up serviceworker.js and manifest.json at the root
urlpatterns = [
    re_path(r'^serviceworker\.js$', ServiceWorker.as_view(), name='serviceworker'),    
    re_path(r'^manifest\.json$', manifest, name='manifest'),
    path('offline/', TemplateView.as_view(template_name="pwa/offline.html"), name="offline"),
]