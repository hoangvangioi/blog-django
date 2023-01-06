from django.contrib.syndication.views import Feed
from django.urls import reverse
from articles.models import Article
from category.models import Category
from django.utils.translation import gettext_lazy as _
from taggit.models import Tag
from django.template.defaultfilters import escape, linebreaksbr
from django.contrib.sites.shortcuts import get_current_site


class LatestArticlesFeed(Feed):

    def __init__(self, *args, **kwargs):
        super(LatestArticlesFeed, self).__init__(*args, **kwargs)
        # self.site = Site.objects.get_current()

    def title(self, request):
        return _(u"%s latest posts") % (get_current_site(request).name, )

    def link(self):
        return reverse("feed_articles")

    def items(self):
        return Article.objects.filter(status='published').order_by('-date_published')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_id(self, item):
        return item.guid

    def item_updated(self, item):
        return item.date_updated

    def item_published(self, item):
        return item.date_published

    def item_content(self, item):
        return {"type" : "html", }, linebreaksbr(escape(item.body))

    def item_links(self, item):
        return [{"href" : reverse("article_detail", args=[item.slug])}]

    def item_authors(self, item):
        return [{"name" : item.author}]


class CategoryFeed(Feed):

    def __init__(self, *args, **kwargs):
        super(CategoryFeed, self).__init__(*args, **kwargs)
        # self.site = Site.objects.get_current()

    def title(self, request):
        return _(u"%s latest posts") % (get_current_site(request).name, )

    def link(self):
        return reverse("feed_categories")

    def items(self):
        return Category.objects.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.name

    def item_link(self, item):
        return reverse('category_articles', args=[item.slug])

    def item_id(self, item):
        return item.guid

    def item_updated(self, item):
        return item.date_created

    def item_published(self, item):
        return item.date_created

    def item_links(self, item):
        return [{"href" : reverse("category_articles", args=[item.slug])}]


class TaggedItemFeed(Feed):

    def __init__(self, *args, **kwargs):
        super(TaggedItemFeed, self).__init__(*args, **kwargs)
        # self.site = Site.objects.get_current()

    def title(self, request, author):
        return _("Posts by %(author_name)s - %(site_name)s") %\
            {'author_name': author, 'site_name': get_current_site(request).name}

    def link(self):
        return reverse('feed_tags')

    def items(self):
        return Tag.objects.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.name

    def item_id(self, item):
        return item.guid

    def item_updated(self, item):
        return item.date_modified

    def item_published(self, item):
        return item.date_created

    def item_link(self, item):
        return reverse('tag_articles', args=[item.slug])

    def item_links(self, item):
        return [{"href" : reverse("tag_articles", args=(item.pk, item.get_slug()))}]