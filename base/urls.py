"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, StaticViewSitemap, CategorySitemap
from django.views.generic import TemplateView
from .feeds import LatestEntriesFeed
from . import views


sitemaps = {
    'static': StaticViewSitemap,
    'post': PostSitemap,
    'category': CategorySitemap,
    # 'profile': ProfileSitemap,
}

urlpatterns = [
    path('hvg/', admin.site.urls),
    # App
    path('', include('post.urls')),
    path('', include('category.urls')),
    path('', include('search.urls')),

    path("user/", include("users.urls")),
    path("comments/", include("django_comments_ink.urls")),

    path('', TemplateView.as_view(template_name='index.html', content_type='text/html'), name='index'), 

    # CKeditor
    re_path(r'^ckeditor/',include('ckeditor_uploader.urls')),

    path('tinymce/', include('tinymce.urls')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='../static/favicon.ico')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain'), name='ads_file'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_file'),

    path('feed', LatestEntriesFeed()),

    path('error/', views.error, name='error')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400 = 'base.views.handler400'
# handler404 = 'base.views.handler404'
# handler500 = 'base.views.handler500'
# handler403 = 'base.views.csrf_failure'


# django.views.defaults.page_not_found
# django.views.defaults.server_error
# django.views.defaults.permission_denied
# django.views.defaults.bad_request


# defaults.page_not_found(request, exception, template_name='404.html')
# defaults.server_error(request, template_name='500.html')
# defaults.permission_denied(request, exception, template_name='403.html')
# defaults.bad_request(request, exception, template_name='400.html')

admin.site.site_header="Blog Hoàng Giỏi Admin"
admin.site.site_title="Blog Hoàng Giỏi Admin Panel"
admin.site.index_title="Welcome to Blog Hoàng Giỏi Admin Panel"