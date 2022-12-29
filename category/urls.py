from django.urls import path
from .views import (
    CategoriesListView,
    CategoryArticlesListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryListView,
)


# CATEGORY URLS #
urlpatterns = [
    # category-articles/<str:slug>/
    path('category/<str:slug>/articles', CategoryArticlesListView.as_view(), name='category_articles'),

    # /categories-list/
    path('categories/list/', CategoriesListView.as_view(), name='categories_list'),

    # Admin categories
    path('create/category/', CategoryCreateView.as_view(), name='create_category'),
    path('category/<slug:slug>/update/', CategoryUpdateView.as_view(), name='update_category'),
    path('category/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='delete_category'),
    path('categories/listadmin/', CategoryListView.as_view(), name='category_list'),
]