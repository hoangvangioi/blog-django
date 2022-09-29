from category.models import Category
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from post.models import Post


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        # return ['post', 'login', 'register', 'logout']
        return ['post', ]

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

    def location(self, item):
        return reverse('post_detail', args=[item.publish.year,
							item.publish.month,
							item.publish.day,
							item.slug])


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return timezone.now()

    def location(self, item):
        return reverse('post_by_category', args=[item.slug])


class ProfileSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Profile.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return reverse('profile', args=[item.slug])
