from .models import Post
from taggit.models import Tag


def sidebar(request):
    most_recent = Post.published.order_by('-created')[:10]
    all_tag = Tag.objects.all()
    all_post = Post.objects.all().order_by('-created')
    context = {
        'most_recent': most_recent,
        'all_tag': all_tag,
        'all_post': all_post,
    }
    return context