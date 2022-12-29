# Core Django imports.
from django.urls import path

# Blog application imports.
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleSearchListView,
    TagArticlesListView,
    ArticleWriteView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleListViewAdmin,
)


# ARTICLE URLS #
urlpatterns = [
    # Home
    path('', ArticleListView.as_view(), name='article_list'),

    # article/<str:slug>/
    path('article/<str:slug>/', ArticleDetailView.as_view(), name='article_detail'),

    # articles/search/?q=query
    path('articles/search/', ArticleSearchListView.as_view(), name='article_search_list_view'),

    # tag/<str:tag_name>/
    path('tag/<str:tag_name>/articles/', TagArticlesListView.as_view(), name="tag_articles"),

    # Admin 
    path('articles/list/', ArticleListViewAdmin.as_view(), name='list_articles_admin'),

    # me/article/write
    path('me/article/write/', ArticleWriteView.as_view(), name="article_write"),

    # me/article/<str:slug>/update/
    path('me/article/<str:slug>/update/', ArticleUpdateView.as_view(), name="article_update"),

    # me/article/<str:slug>/delete/
    path('me/article/<str:slug>/delete/', ArticleDeleteView.as_view(), name="article_delete"),
]