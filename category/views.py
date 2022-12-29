from django.contrib.auth.mixins import (LoginRequiredMixin,
										PermissionRequiredMixin)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from articles.models import Article

from .decorators import superuser_required
from .forms import CategoryForm
from .models import Category
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator

# Create your views here.


@method_decorator(superuser_required, name='dispatch')
class CategoryListView(LoginRequiredMixin, ListView):
	model = Category
	template_name = 'category/category_list_form.html'
	context_object_name = 'category'
	ordering = ['-id']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Lists of Category'
		context['head_title'] = 'Lists of Category'
		return context


@method_decorator(superuser_required, name='dispatch')
class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Category
	template_name = "category/create_category.html"
	form_class = CategoryForm
	success_message = "Category Created Successfully"

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, f"'{form.instance.name}' "
								f"submitted successfully. You will be "
								f"notified when it is approved."
								f"Thank you !!!")
		return super().form_valid(form)


@method_decorator(superuser_required, name='dispatch')
class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Category
	template_name = "category/update_category.html"
	form_class = CategoryForm
	success_message = "Category Updated Successfully"

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


@method_decorator(superuser_required, name='dispatch')
class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Category
	template_name = "category/delete_category.html"
	success_url = reverse_lazy('category_list')
	success_message = "Category deleted successfully"


class CategoriesListView(ListView):
    model = Category
    paginate_by = 12
    context_object_name = 'categories'
    template_name = 'category/categories_list.html'

    def get_queryset(self):
        return Category.objects.order_by('-date_created')


class CategoryArticlesListView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'articles'
    template_name = 'category/category_articles.html'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Article.objects.filter(category=category, status='published')

    def get_context_data(self, **kwargs):
        context = super(CategoryArticlesListView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context['category'] = category
        return context