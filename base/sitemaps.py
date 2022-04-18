from category.models import Category
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from post.models import Post


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['post', 'login', 'register']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.id
