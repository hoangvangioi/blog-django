from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from .models import Post
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
# from .decorators import superuser_required
from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .forms import CommentForm
from .decorators import superuser_required


# Create your views here.


class PostListView(ListView):
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
from django.contrib import messages


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:5]
    current_site = get_current_site(request)

    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    user_comment = None
    redirect_url = post.get_absolute_url()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.user = request.user
            user_comment.post = post
            user_comment.save()
            return redirect(redirect_url)
    else:
        comment_form = CommentForm()

    context = {'domain': current_site,
                'post': post,
                'similar_posts': similar_posts,
                'comments':  user_comment,
                'comments': comments,
                'comment_form': comment_form,
                'allcomments': allcomments,
                }
    return render(request, 'post/post_detail.html', context)


@method_decorator(superuser_required, name='dispatch')
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
# class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "post/create_post.html"
    permission_required = 'post.fields'

    def form_valid(self, form):
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

class PostUpdateView(UpdateView):
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

class PostDeleteView(DeleteView):
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