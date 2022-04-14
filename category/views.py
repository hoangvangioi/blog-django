from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from post.models import Post

from .forms import CategoryForm
from .models import Category

# Create your views here.


class CategoryListView(ListView):
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


class CategoryCreateView(CreateView):
    model = Category
    template_name = "category/create_category.html"
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "category/update_category.html"
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category/delete_category.html"
    success_url = reverse_lazy('post')


class ListCategoryView(ListView):
	model = Category
	template_name = 'category/list_category.html'
	context_object_name = 'list_category'
	queryset = Category.objects.all()
