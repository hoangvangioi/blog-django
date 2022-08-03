from .models import Post
from taggit.models import Tag


def sidebar(request):
    most_recent = Post.published.order_by('-created')[:10]
    all_tag = Tag.objects.all()
    context = {
        'most_recent': most_recent,
        'all_tag': all_tag,
    }
    return context