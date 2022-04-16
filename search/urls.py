from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('post/search/', views.search_post, name='search_post'),
]
