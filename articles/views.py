# Standard Python Library imports.
from functools import reduce
import operator

# Core Django imports.
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _

# Blog application imports.
from .decorators import superuser_required
from .models import check_comments_input_allowed
from .models import Article
from category.models import Category
from taggit.models import Tag
from .forms import ArticleForm


class ArticleListView(ListView):
    context_object_name = "articles"
    paginate_by = 12
    queryset = Article.objects.filter(status='published')
    template_name = "articles/article_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        paginator = Paginator(self.queryset, self.paginate_by)
        page_number = self.request.GET.get("page", 1)
        page_object = paginator.get_page(page_number)
        page_object.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
        context['page_obj'] = page_object
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        session_key = f"viewed_article {self.object.slug}"
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True
            
        kwargs['related_articles'] = Article.objects.filter(category=self.object.category, status='published').order_by('?')[:3]
        kwargs['latest_articles'] = Article.objects.filter(status='published').order_by('-date_created')[:5]
        kwargs['categories'] = Category.objects.all()
        kwargs['article'] = self.object
        kwargs['list_tags'] = Tag.objects.all()
        kwargs['next'] = reverse("comments-ink-sent")
        kwargs['is_comment_input_allowed'] = check_comments_input_allowed(get_object_or_404(Article, slug=self.object.slug, status='published')),
        return super().get_context_data(**kwargs)


class ArticleSearchListView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'search_results'
    template_name = "articles/article_search_list.html"

    def get_queryset(self):
        """
        Search for a user input in the search bar.

        It pass in the query value to the search view using the 'q' parameter.
        Then in the view, It searches the 'title', 'slug', 'body' and fields.

        To make the search a little smarter, say someone searches for
        'container docker ansible' and It want to search the records where all
        3 words appear in the article content in any order, It split the query
        into separate words and chain them.
        """

        query = self.request.GET.get('q')

        if query:
            query_list = query.split()
            print(query_list)
            search_results = Article.objects.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(slug__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(body__icontains=q) for q in query_list))
            )

            if not search_results:
                messages.info(self.request, f"No results for '{query}'")
                return search_results.filter(status='published')
            else:
                messages.success(self.request, f"Results for '{query}'")
                return search_results.filter(status='published')
        else:
            messages.error(self.request, f"Sorry you did not enter any keyword")
            return []

    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(ArticleSearchListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['articles'] = Article.objects.filter(status='published')
        return context


class TagArticlesListView(ListView):
    """
        List articles related to a tag.
    """
    model = Article
    paginate_by = 12
    context_object_name = 'tag_articles_list'
    template_name = 'articles/tag_articles_list.html'

    def get_queryset(self):
        """
            Filter Articles by tag_name
        """
        tag_name = self.kwargs.get('tag_name', '')

        if tag_name:
            tag_articles_list = Article.objects.filter(tags__name__in=[tag_name],
                                                       status='published')

            if not tag_articles_list:
                messages.info(self.request, f"No Results for '{tag_name}' tag")
                return tag_articles_list
            else:
                messages.success(self.request, f"Results for '{tag_name}' tag")
                return tag_articles_list
        else:
            messages.error(self.request, "Invalid tag")
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(superuser_required, name='dispatch')
class ArticleWriteView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/create_article.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        context['submit'] = 'Create Article'
        context['head_title'] = 'Create Article'
        return context


@method_decorator(superuser_required, name='dispatch')
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "articles/update_article.html"
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        context['submit'] = 'Update Article'
        context['head_title'] = 'Update Article'
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@method_decorator(superuser_required, name='dispatch')
class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "articles/delete_article.html"
    success_url = reverse_lazy('list_articles_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete'
        context['submit'] = 'Delete Article'
        context['head_title'] = 'Delete Article'
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@method_decorator(superuser_required, name='dispatch')
class ArticleListViewAdmin(LoginRequiredMixin, ListView, PermissionRequiredMixin):
	model = Article
	template_name = 'articles/article_list_form.html'
	context_object_name = 'post'
	ordering = ['-id']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Lists of Article'
		context['head_title'] = 'Lists of Article'
		return context