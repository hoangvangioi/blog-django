from category.models import Category
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from articles.models import Article
from taggit.models import Tag, TaggedItem


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['article_list', 'categories_list', 'login', 'register', ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return timezone.now()


class ArticlesSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Article.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.date_published

    def location(self, item):
        return reverse('article_detail', args=[item.slug])


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return timezone.now()

    def location(self, item):
        return reverse('category_articles', args=[item.slug])


class TagSitemap(Sitemap):
    """
    Sitemap for tags.
    """

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return timezone.now()

    def location(self, item):
        return reverse('tag_articles', args=[item.slug])