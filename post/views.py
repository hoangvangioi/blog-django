from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from taggit.models import Tag

from .decorators import superuser_required
from .forms import PostForm
from .models import Post
from django.urls import reverse
from .models import check_comments_input_allowed
from django.db.models import Q


# Create your views here.


@method_decorator(superuser_required, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'post/post_list_form.html'
	context_object_name = 'post'
	ordering = ['-id']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Lists of Post'
		context['head_title'] = 'Lists of Post'
		return context


def post_list(request, tag_slug=None):
    posts = Post.published.all()

    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 10)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    context = {'posts': posts, 
                'pages': page, 
                'tag': tag,
                }

    return render(request, 'post/post_list.html', context)


def search_post(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            posts = Post.objects.order_by('-publish').filter(Q(title__icontains=keyword) | Q(body__icontains=keyword))
            post_count = posts.count()
        else:
            # If not searched, return default posts
            posts = Post.objects.all().order_by("-publish")
            post_count = 0
    context = {
        'posts': posts,
        'post_count': post_count,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    current_site = get_current_site(request)

    context = {'domain': current_site,
                'post': post,
                'similar_posts': similar_posts,
                "next": reverse("comments-ink-sent"),
                "is_comment_input_allowed": check_comments_input_allowed(post),
                }
    return render(request, 'post/post_detail.html', context)


@method_decorator(superuser_required, name='dispatch')
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post/create_post.html"
    permission_required = 'post.fields'

    def form_valid(self, form):
        post_form = super(PostCreateView, self).form_valid(form)
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        context['submit'] = 'Create Post'
        context['head_title'] = 'Create Post'
        return context


@method_decorator(superuser_required, name='dispatch')
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "post/update_post.html"
    form_class = PostForm
    # slug_field = 'post'
    slug_url_kwarg = 'post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        context['submit'] = 'Update Post'
        context['head_title'] = 'Update Post'
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@method_decorator(superuser_required, name='dispatch')
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "post/delete_post.html"
    success_url = reverse_lazy('post')
    slug_url_kwarg = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete'
        context['submit'] = 'Delete Post'
        context['head_title'] = 'Delete Post'
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
