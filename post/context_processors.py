from .models import Post
from django.db.models import Count
from taggit.models import Tag


def get_category_count():
	category_query = Post.published.values('categories__slug', 'categories__title')
	return category_query

def sidebar(request):
	# category_count = get_category_count()
	most_recent = Post.published.order_by('-created')[:5]
	all_tag = Tag.objects.all()
	context = {
		'most_recent': most_recent,
		'all_tag': all_tag,
		# 'category_count': category_count,
	}
	return context