from django.contrib.sitemaps import Sitemap
# from post.models import Post

from django.urls import reverse

from post.models import Post


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['post']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated