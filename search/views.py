from django.shortcuts import render
from django.db.models import Q
from post.models import Post


# Create your views here.


def search_post(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            posts = Post.objects.order_by('-publish').filter(Q(title__icontains=keyword) | Q(body__icontains=keyword))
            post_count = posts.count()
    context = {
        'posts': posts,
        'post_count': post_count,
    }
    return render(request, 'post/post_list.html', context)