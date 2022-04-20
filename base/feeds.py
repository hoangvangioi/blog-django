from django.contrib.syndication.views import Feed
from django.urls import reverse
from post.models import Post


class LatestEntriesFeed(Feed):
    title = "Hoangvangioi.xyz: New article for Python programmers every week"
    link = "/feed/"
    description = "Updates on changes and additions to python articles on pythoncircle.com."

    def items(self):
        return Post.objects.order_by('-updated')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

#    item_link is only needed if Post has no get_absolute_url method.
    def item_link(self, item):
        return reverse('post_detail', args=[item.publish.year,
							item.publish.month,
							item.publish.day,
							item.slug])