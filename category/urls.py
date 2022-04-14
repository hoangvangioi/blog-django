from django.urls import path
from .views import *


urlpatterns = [
	path('category/<slug:slug>/', PostCategoryView.as_view(), name='post_by_category'),
    path('create/category/', CategoryCreateView.as_view(), name='create_category'),
    path('category/<slug:slug>/update/', CategoryUpdateView.as_view(), name='update_category'),
    path('category/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='delete_category'),
    # path('list/category/', ListCategoryView.as_view(), name='list_category'),
    path('list/category/', CategoryListView.as_view(), name='category_list'),

]