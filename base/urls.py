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
from .sitemaps import ArticlesSitemap, StaticViewSitemap, CategorySitemap, TagSitemap
from django.views.generic import TemplateView
from .feeds import LatestArticlesFeed, TaggedItemFeed, CategoryFeed
from . import views
from .views import AboutPageView, PrivacyPolicyView

sitemaps = {
    'static': StaticViewSitemap,
    'article': ArticlesSitemap,
    'category': CategorySitemap,
    'tags': TagSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admindocs/', include('django.contrib.admindocs.urls')),

    # App
    path('', include('articles.urls')),
    path('', include('category.urls')),

    path("", include("users.urls")),
    path("comments/", include("django_comments_ink.urls")),

    # CKeditor
    re_path(r'^ckeditor/',include('ckeditor_uploader.urls')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='../static/favicon.svg')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('ads.txt', TemplateView.as_view(template_name='ads.txt', content_type='text/plain'), name='ads_file'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_file'),

    path('feed/articles/', LatestArticlesFeed(), name='feed_articles'),
    path('feed/categories/', CategoryFeed(), name= 'feed_categories'),
    path('feed/tags/', TaggedItemFeed(), name='feed_tags'),
    path('maintenance/', TemplateView.as_view(template_name='error/503.html', content_type='text/html'), name='maintenance'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path("contact/", include("contact.urls")),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'base.views.handler400'
handler403 = 'base.views.handler403'
handler404 = 'base.views.handler404'
handler500 = 'base.views.handler500'


admin.site.site_header="Blog Hoàng Giỏi Admin"
admin.site.site_title="Blog Hoàng Giỏi Admin Panel"
admin.site.index_title="Welcome to Blog Hoàng Giỏi Admin Panel"


try:
    from .local_urls import *
except ImportError:
    pass