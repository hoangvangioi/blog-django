from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from post.models import Post

from .decorators import superuser_required
from .forms import CategoryForm
from .models import Category


# Create your views here.


@method_decorator(superuser_required, name='dispatch')
class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Category
	template_name = 'category/category_list_form.html'
	context_object_name = 'category'
	ordering = ['-id']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Lists of Category'
		context['head_title'] = 'Lists of Category'
		return context


class PostCategoryView(ListView):
	model = Post
	template_name = 'post/post_list.html'
	context_object_name = 'posts'
	ordering = ['-created']
	queryset = Category.objects.all()

	def get_queryset(self):
		cat = Category.objects.all()
		self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
		return Post.published.filter(category = self.category)

	def get_context_data(self, **kwargs):
		context = super(PostCategoryView, self).get_context_data(**kwargs)
		context['category'] = self.category
		return context


@method_decorator(superuser_required, name='dispatch')
class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = "category/create_category.html"
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(superuser_required, name='dispatch')
class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = "category/update_category.html"
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(superuser_required, name='dispatch')
class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = "category/delete_category.html"
    success_url = reverse_lazy('post')


@method_decorator(superuser_required, name='dispatch')
class ListCategoryView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	model = Category
	template_name = 'category/list_category.html'
	context_object_name = 'list_category'
	queryset = Category.objects.all()