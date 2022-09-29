from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path('blog/', views.post_list, name='post'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_tag'),
    path('post/create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/update/', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('post/list/', PostListView.as_view(), name='list_post'),
]
