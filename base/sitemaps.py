from django.utils import timezone
from category.models import Category
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from post.models import Post
from accounts.models import Profile


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return ['post', 'login', 'register']

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return timezone.now()

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return timezone.now()


class ProfileSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Profile.objects.all()

    def lastmod(self, obj):
        return obj.updated_at